"""Gold-blind, deterministic context packets for matched localization treatments."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from time import perf_counter, process_time

from .inference import PreparedInference, rank_files
from .records import digest, encoded, jsonl, read_jsonl, write_artifacts

PROFILE = "bm25-top20-prefix1200-v1"
TOP_FILES = 20
PREFIX_CHARACTERS = 1200


def packet(record: dict) -> tuple[dict, dict]:
    prepared = PreparedInference.from_record(record)
    task = prepared.instance
    paths = set(rank_files(task, TOP_FILES)) if prepared.preparation_status == "prepared" else set()
    candidates = [
        {"path": candidate.path, "text": candidate.text[:PREFIX_CHARACTERS]}
        for candidate in sorted(task.candidates, key=lambda c: c.path)
        if candidate.path in paths
    ]
    narrowed = {
        **record,
        "instance": {**record["instance"], "candidates": candidates},
        "candidate_sha256": digest(encoded(candidates)),
    }
    PreparedInference.from_record(narrowed)
    source = {c.path: c for c in task.candidates}
    provenance = {
        "schema_version": "1.0.0",
        "instance_id": task.instance_id,
        "profile": PROFILE,
        "source_candidate_sha256": prepared.candidate_sha256,
        "context_candidate_sha256": narrowed["candidate_sha256"],
        "full_candidate_count": len(task.candidates),
        "context_candidate_count": len(candidates),
        "issue_sha256": digest(task.issue.encode()),
        "excerpts": [
            {
                "path": c["path"],
                "original_characters": len(source[c["path"]].text),
                "shown_characters": len(c["text"]),
                "truncated": len(source[c["path"]].text) > PREFIX_CHARACTERS,
                "excerpt_sha256": digest(c["text"].encode()),
            }
            for c in candidates
        ],
    }
    return narrowed, provenance


def prepare_context(inputs: Path, output: Path, synthetic: bool = False) -> dict:
    if output.exists():
        raise ValueError("Output exists; context packets cannot be overwritten")
    source = read_jsonl(inputs)
    ids = [r["instance"]["instance_id"] for r in source]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Input IDs must be nonempty and unique")
    tasks, provenance = [], []
    for record in source:
        wall, cpu = perf_counter(), process_time()
        narrowed, metadata = packet(record)
        metadata["wall_ms"] = (perf_counter() - wall) * 1000
        metadata["cpu_ms"] = (process_time() - cpu) * 1000
        tasks.append(narrowed)
        provenance.append(metadata)
    manifest = {
        "schema_version": "1.0.0",
        "program": "context",
        "profile": PROFILE,
        "synthetic": synthetic,
        "input_sha256": digest(inputs.read_bytes()),
        "tasks_sha256": digest(jsonl(tasks)),
        "selected": len(tasks),
        "config": {
            "retrieval": "lexical-bm25-v1",
            "top_files": TOP_FILES,
            "prefix_characters": PREFIX_CHARACTERS,
            "candidate_order": "lexicographic-path",
            "issue_policy": "full-unmodified",
        },
        "wall_ms_total": sum(p["wall_ms"] for p in provenance),
        "cpu_ms_total": sum(p["cpu_ms"] for p in provenance),
        "measurement_boundary": "input validation, retrieval and packet construction; excludes I/O",
        "monetary_usd": None,
        "gpu_seconds": 0,
        "python": platform.python_version(),
        "runtime_sources": {
            name: digest((Path(__file__).parent / name).read_bytes())
            for name in ("__init__.py", "context.py", "inference.py", "records.py")
        },
    }
    write_artifacts(
        output,
        {
            "tasks.jsonl": jsonl(tasks),
            "context.jsonl": jsonl(provenance),
            "manifest.json": encoded(manifest),
        },
    )
    return {"selected": len(tasks), "profile": PROFILE}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(prepare_context(**vars(args)), indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
