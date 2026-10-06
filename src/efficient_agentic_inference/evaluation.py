"""Standalone evaluator of saved immutable predictions and separate labels."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from .inference import prediction_error
from .labeler import EvaluationInstance
from .metrics import KS, evaluate
from .records import digest, encoded, jsonl, read_jsonl, verify_artifacts, write_artifacts


def quality(prediction: dict, paths: list[str], known: bool) -> dict:
    if not known:
        return {
            "recall_at_k": {str(k): None for k in KS},
            "precision_at_k": {str(k): None for k in KS},
            "strict_success_at_k": {str(k): None for k in KS},
            "mrr": None,
            "gold_file_count": None,
            "candidate_recall_ceiling": None,
            "conditional_recall_at_k": {str(k): None for k in KS},
        }
    metrics = evaluate(prediction["ranked_files"], paths, prediction["disposition"])
    available = set(paths) & set(prediction["candidate_paths"])
    usable = prediction["ranked_files"] if prediction["disposition"] == "valid" else []
    metrics["candidate_recall_ceiling"] = len(available) / len(paths) if paths else None
    metrics["conditional_recall_at_k"] = {
        str(k): len(set(usable[:k]) & available) / len(available) if available else None for k in KS
    }
    return metrics


def mean_defined(values: list) -> float | None:
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def observed_sum(values: list[float | None]) -> float | None:
    """Sum known measurements; no observations is unknown, not measured zero."""
    known = [v for v in values if v is not None]
    return sum(known) if known else None


def aggregate(records: list[dict], subset: str) -> dict:
    metrics = [r[subset] for r in records]
    unknown = sum(m["gold_file_count"] is None for m in metrics)
    nonempty = sum(bool(m["gold_file_count"]) for m in metrics)
    return {
        "unknown_label_tasks": unknown,
        "nonempty_gold_tasks": nonempty,
        "empty_gold_tasks": sum(m["gold_file_count"] == 0 for m in metrics),
        "mean_recall_at_k": {
            str(k): mean_defined([m["recall_at_k"][str(k)] for m in metrics])
            if not unknown
            else None
            for k in KS
        },
        "known_label_mean_recall_at_k": {
            str(k): mean_defined([m["recall_at_k"][str(k)] for m in metrics]) for k in KS
        },
        "mean_precision_at_k": {
            str(k): mean_defined([m["precision_at_k"][str(k)] for m in metrics])
            if not unknown
            else None
            for k in KS
        },
        "mrr": mean_defined([m["mrr"] for m in metrics]) if not unknown else None,
        "strict_successes_at_5": sum(m["strict_success_at_k"]["5"] is True for m in metrics),
        "strict_success_rate_at_5": sum(m["strict_success_at_k"]["5"] is True for m in metrics)
        / len(records)
        if not unknown
        else None,
        "candidate_recall_ceiling": mean_defined([m["candidate_recall_ceiling"] for m in metrics])
        if not unknown
        else None,
        "conditional_recall_at_k": {
            str(k): mean_defined([m["conditional_recall_at_k"][str(k)] for m in metrics])
            if not unknown
            else None
            for k in KS
        },
        "conditional_denominator_tasks": sum(
            m["conditional_recall_at_k"]["5"] is not None for m in metrics
        ),
    }


def evaluate_saved(prediction_dir: Path, gold: Path, output: Path) -> dict:
    if output.exists():
        raise ValueError("Output exists; evaluation cannot overwrite records")
    checksums = verify_artifacts(prediction_dir)
    if "predictions.jsonl" not in checksums or "manifest.json" not in checksums:
        raise ValueError("Missing prediction artifacts in checksum manifest")
    prediction_bytes = (prediction_dir / "predictions.jsonl").read_bytes()
    inference_manifest = json.loads((prediction_dir / "manifest.json").read_text())
    if (prediction_dir / "predictions.sha256").read_text().strip() != digest(prediction_bytes):
        raise ValueError("Prediction checksum mismatch")
    predictions = read_jsonl(prediction_dir / "predictions.jsonl")
    evaluations = [EvaluationInstance.from_record(r) for r in read_jsonl(gold)]
    by_id = {r.instance_id: r for r in evaluations}
    ids = [p["instance_id"] for p in predictions]
    if (
        not ids
        or len(set(ids)) != len(ids)
        or len(by_id) != len(evaluations)
        or set(ids) != set(by_id)
    ):
        raise ValueError("Prediction/label IDs must match exactly and be unique")
    records = []
    for prediction in predictions:
        if prediction_error(prediction["candidate_paths"], set(prediction["candidate_paths"])):
            raise ValueError("Invalid candidate paths in prediction artifact")
        if prediction["disposition"] == "valid" and prediction_error(
            prediction["ranked_files"], set(prediction["candidate_paths"])
        ):
            raise ValueError("Prediction marked valid violates output contract")
        evaluation = by_id[prediction["instance_id"]]
        known = evaluation.label_status in {"labeled", "empty_patch"}
        all_paths = [c["path"] for c in evaluation.changes]
        implementation = [
            c["path"] for c in evaluation.changes if c["category"] == "implementation"
        ]
        records.append(
            {
                "instance_id": prediction["instance_id"],
                "disposition": prediction["disposition"],
                "label_status": evaluation.label_status,
                "failure_reason": evaluation.failure_reason,
                "all_files": quality(prediction, all_paths, known),
                "implementation_files": quality(prediction, implementation, known),
            }
        )
    wall = sorted(
        p["measurements"]["wall_ms"]
        for p in predictions
        if p["measurements"]["wall_ms"] is not None
    )
    costs = [p["measurements"]["monetary_usd"] for p in predictions]
    total_cost = sum(costs) if all(c is not None for c in costs) else None
    all_metrics = aggregate(records, "all_files")
    successes = all_metrics["strict_successes_at_5"]
    summary = {
        "schema_version": "2.0.0",
        "contract": "localization-v2",
        "synthetic": inference_manifest["synthetic"],
        "predictions_sha256": digest(prediction_bytes),
        "gold_sha256": digest(gold.read_bytes()),
        "selected": len(predictions),
        "prepared": sum(p["disposition"] != "preparation_failed" for p in predictions),
        "failed_preparation": sum(p["disposition"] == "preparation_failed" for p in predictions),
        "failed_prediction": sum(
            p["disposition"] not in {"valid", "preparation_failed"} for p in predictions
        ),
        "all_files": all_metrics,
        "implementation_files": aggregate(records, "implementation_files"),
        "wall_ms_p50": wall[math.ceil(0.5 * len(wall)) - 1] if wall else None,
        "wall_ms_p95": wall[math.ceil(0.95 * len(wall)) - 1] if wall else None,
        "latency_tasks": len(wall),
        "cpu_ms_total_observed": observed_sum([p["measurements"]["cpu_ms"] for p in predictions]),
        "gpu_seconds": sum(p["measurements"]["gpu_seconds"] for p in predictions)
        if all(p["measurements"]["gpu_seconds"] is not None for p in predictions)
        else None,
        "total_monetary_usd": total_cost,
        "cost_per_success_usd": total_cost / successes
        if total_cost is not None and successes and not all_metrics["unknown_label_tasks"]
        else None,
        "cost_reason": "unknown_cost"
        if total_cost is None
        else (
            "unknown_labels"
            if all_metrics["unknown_label_tasks"]
            else ("zero_successes" if not successes else None)
        ),
        "quantile_method": "nearest-rank",
    }
    write_artifacts(output, {"summary.json": encoded(summary), "metrics.jsonl": jsonl(records)})
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(evaluate_saved(args.predictions, args.gold, args.output), indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
