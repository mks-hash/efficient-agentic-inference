"""CPU fixture runner. Model and SWE-bench acquisition are intentionally deferred."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from jsonschema import Draft202012Validator, FormatChecker

from . import __version__
from .localization import Task, evaluate, prediction_error, rank_files, summarize, valid_path

GATES = (
    "identity",
    "render",
    "token_provenance",
    "output_contract",
    "resource_fit",
    "useful_localization",
    "trainability",
    "frozen_evaluation",
    "economics",
    "generalization",
    "systems",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def validate(record: dict, schema: Path) -> None:
    spec = json.loads(schema.read_text())
    Draft202012Validator.check_schema(spec)
    Draft202012Validator(spec, format_checker=FormatChecker()).validate(record)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def git_value(root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def source_hash(root: Path) -> str:
    """Hash relevant source bytes, including uncommitted implementation changes."""
    paths = [root / "pyproject.toml", root / "uv.lock"]
    for folder in ("src", "schemas", "tests", "examples", "docs"):
        paths.extend((root / folder).rglob("*"))
    payload = hashlib.sha256()
    for path in sorted(set(paths)):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        payload.update(str(path.relative_to(root)).encode() + b"\0")
        payload.update(digest(path.read_bytes()).encode() + b"\0")
    return payload.hexdigest()


def run(args: argparse.Namespace) -> dict:
    root = args.project_root.resolve()
    tasks = [Task.from_record(record) for record in read_jsonl(args.tasks)]
    ids = [task.instance_id for task in tasks]
    if not tasks or len(set(ids)) != len(ids):
        raise ValueError("Tasks must be nonempty and instance IDs unique")
    gold = {}
    for record in read_jsonl(args.gold):
        if not isinstance(record, dict) or set(record) != {"instance_id", "changed_files"}:
            raise ValueError("Gold fields must be instance_id and changed_files")
        instance_id, paths = record["instance_id"], record["changed_files"]
        if not isinstance(instance_id, str) or not instance_id or instance_id in gold:
            raise ValueError("Gold instance IDs must be nonempty and unique")
        if not isinstance(paths, list) or any(not valid_path(path) for path in paths):
            raise ValueError("Invalid gold paths")
        if len(set(paths)) != len(paths):
            raise ValueError("Duplicate gold paths")
        gold[instance_id] = paths
    if set(gold) != set(ids):
        raise ValueError("Task and gold instance ID sets must match exactly")
    if args.output.exists():
        raise ValueError("Output exists; immutable runs cannot be overwritten")
    if args.limit < 10:
        raise ValueError("limit must be >=10 to support all declared metric K values")

    config = {"limit": args.limit, "k1": 1.2, "b": 0.75, "primary_k": 5}
    results = []
    for task in tasks:
        started = perf_counter()
        failure = None
        try:
            ranked = rank_files(task, args.limit)
            failure = prediction_error(ranked, {c.path for c in task.candidates})
            disposition = "invalid_output" if failure else "valid"
            raw = json.dumps(ranked)
            normalized = [] if failure else ranked
        except Exception as exc:
            # An individual failed attempt must survive evaluation and accounting.
            raw = None
            normalized = []
            disposition = "runtime_error"
            failure = f"{type(exc).__name__}: {exc}"
        elapsed = (perf_counter() - started) * 1000
        record = {
            "schema_version": "1.0.0",
            "run_id": args.output.name,
            "instance_id": task.instance_id,
            "ranked_files": normalized,
            "disposition": disposition,
            "failure_reason": failure,
            "raw_output": raw,
            "metrics": evaluate(normalized, gold[task.instance_id], disposition),
            "measurements": {
                "wall_ms": elapsed,
                "input_tokens": None,
                "output_tokens": None,
                "gpu_seconds": 0,
                "monetary_usd": None,
                "unknown_reasons": [
                    "CPU cost not priced",
                    "Tokens inapplicable to lexical ranking",
                ],
            },
            "fallback": {
                "used": False,
                "reason": None,
                "model_revision": None,
                "wall_ms": 0,
                "monetary_usd": 0,
            },
        }
        validate(record, root / "schemas/v1/result.schema.json")
        results.append(record)

    evidence = {
        gate: {"status": "NOT_RUN", "reason": "Synthetic software fixture, no model evidence"}
        for gate in GATES
    }
    for gate in ("token_provenance", "resource_fit", "trainability", "systems"):
        evidence[gate] = {"status": "UNSUPPORTED", "reason": "CPU lexical baseline; no model"}
    evidence["economics"] = {"status": "UNKNOWN", "reason": "CPU monetary cost not priced"}
    manifest = {
        "schema_version": "1.0.0",
        "benchmark_contract": "localization-v1",
        "run_id": args.output.name,
        "created_at": datetime.now(UTC).isoformat(),
        "synthetic": True,
        "code": {
            "git_commit": git_value(root, "rev-parse", "HEAD"),
            "dirty": git_value(root, "status", "--porcelain") != "",
            "source_sha256": source_hash(root),
        },
        "dataset": {
            "name": "synthetic-localization-fixture",
            "revision": None,
            "split": "fixture",
            "tasks_sha256": digest(args.tasks.read_bytes()),
            "gold_sha256": digest(args.gold.read_bytes()),
            "task_ids_sha256": digest(encoded(ids)),
            "label_policy": "manually-specified-fixture-v1",
            "leakage_policy": "separate-gold-and-canonical-task-v1",
        },
        "model": None,
        "variant": {
            "kind": "lexical",
            "adapter_revision": None,
            "prompt_sha256": None,
            "retrieval_profile": "lexical-bm25-v1",
            "config_sha256": digest(encoded(config)),
        },
        "config": config,
        "hardware": {"cpu": platform.machine(), "gpu": None, "gpu_count": 0},
        "environment": {
            "python": platform.python_version(),
            "backend": "stdlib-bm25",
            "backend_version": __version__,
        },
        "cost_model": {
            "currency": "USD",
            "rate_usd_per_hour": None,
            "price_source": None,
            "price_snapshot_date": None,
            "allocation_boundary": "unpriced CPU ranking only",
            "training_usd": 0,
        },
        "accounting": {
            "latency_boundary": (
                "per-task ranking, validation and raw serialization; excludes I/O/evaluation"
            ),
            "unknown_reasons": ["CPU monetary cost not priced; CPS unavailable"],
        },
        "evidence": evidence,
        "artifacts": {
            "predictions": "predictions.jsonl",
            "summary": "summary.json",
            "checksums": "checksums.json",
        },
    }
    validate(manifest, root / "schemas/v1/experiment.schema.json")
    summary = {"synthetic": True, "run_id": args.output.name, **summarize(results)}
    # Atomic directory creation prevents concurrent runs from overwriting a run.
    args.output.mkdir(parents=True, exist_ok=False)
    artifacts = {
        "manifest.json": encoded(manifest),
        "summary.json": encoded(summary),
        "predictions.jsonl": b"".join(
            (json.dumps(record, sort_keys=True) + "\n").encode() for record in results
        ),
    }
    for name, payload in artifacts.items():
        (args.output / name).write_bytes(payload)
    (args.output / "checksums.json").write_bytes(
        encoded({name: digest(payload) for name, payload in artifacts.items()})
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Efficient Agentic Inference CPU fixture runner")
    commands = parser.add_subparsers(dest="command", required=True)
    baseline = commands.add_parser(
        "baseline", help="Run lexical BM25 on synthetic canonical inputs"
    )
    baseline.add_argument("--tasks", type=Path, required=True)
    baseline.add_argument("--gold", type=Path, required=True)
    baseline.add_argument("--output", type=Path, required=True)
    baseline.add_argument("--project-root", type=Path, default=Path.cwd())
    baseline.add_argument("--limit", type=int, default=10)
    baseline.add_argument("--synthetic", action="store_true", required=True)
    args = parser.parse_args()
    try:
        summary = run(args)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(json.dumps(summary, indent=2), file=sys.stdout)
