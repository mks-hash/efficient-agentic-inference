"""Standalone stdlib inference program. Accepts only inference records."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from time import perf_counter, process_time

from .inference import PreparedInference, prediction_error, rank_files
from .records import digest, encoded, jsonl, read_jsonl, write_artifacts


def predict(inputs: Path, output: Path, limit: int = 10, synthetic: bool = False) -> dict:
    if output.exists():
        raise ValueError("Output exists; runs cannot be overwritten")
    if limit < 10:
        raise ValueError("limit must be >=10")
    instances = [PreparedInference.from_record(r) for r in read_jsonl(inputs)]
    ids = [item.instance.instance_id for item in instances]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Instance IDs must be nonempty and unique")
    predictions = []
    for prepared in instances:
        task = prepared.instance
        wall, cpu = perf_counter(), process_time()
        ranked, raw, reason = [], None, prepared.failure_reason
        if prepared.preparation_status != "prepared":
            disposition = "preparation_failed"
        else:
            try:
                ranked = rank_files(task, limit)
                raw = json.dumps(ranked)
                reason = prediction_error(ranked, {c.path for c in task.candidates})
                disposition = "invalid_output" if reason else "valid"
                if reason:
                    ranked = []
            except Exception as exc:
                ranked = []
                disposition = "runtime_error"
                reason = f"{type(exc).__name__}: {exc}"
        predictions.append(
            {
                "schema_version": "2.0.0",
                "instance_id": task.instance_id,
                "ranked_files": ranked,
                "raw_output": raw,
                "disposition": disposition,
                "failure_reason": reason,
                "candidate_paths": [c.path for c in task.candidates],
                "candidate_sha256": prepared.candidate_sha256,
                "measurements": {
                    "wall_ms": (perf_counter() - wall) * 1000
                    if disposition != "preparation_failed"
                    else None,
                    "cpu_ms": (process_time() - cpu) * 1000
                    if disposition != "preparation_failed"
                    else None,
                    "input_tokens": None,
                    "output_tokens": None,
                    "gpu_seconds": 0,
                    "monetary_usd": None,
                },
            }
        )
    runtime = {
        name: digest((Path(__file__).parent / name).read_bytes())
        for name in ("__init__.py", "inference.py", "predict.py", "records.py")
    }
    manifest = {
        "schema_version": "2.0.0",
        "program": "predict",
        "synthetic": synthetic,
        "inputs_sha256": digest(inputs.read_bytes()),
        "runtime_sources": runtime,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "config": {"ranker": "lexical-bm25-v1", "limit": limit, "k1": 1.2, "b": 0.75},
        "latency_boundary": "ranking, validation and serialization; excludes I/O/evaluation",
        "cost_reason": "CPU cost not priced; tokens inapplicable; no accelerator used",
    }
    write_artifacts(
        output,
        {
            "predictions.jsonl": jsonl(predictions),
            "manifest.json": encoded(manifest),
            "predictions.sha256": (digest(jsonl(predictions)) + "\n").encode(),
        },
    )
    return {
        "attempted": len(predictions),
        "valid": sum(p["disposition"] == "valid" for p in predictions),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(predict(args.inputs, args.output, args.limit, args.synthetic), indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
