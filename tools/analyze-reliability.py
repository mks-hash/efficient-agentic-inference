#!/usr/bin/env python3
"""Compare immutable four-arm predictions/evaluations after all inference completes."""

import argparse
import json
from pathlib import Path

from efficient_agentic_inference.records import (
    digest,
    encoded,
    read_jsonl,
    verify_artifacts,
    write_artifacts,
)
from efficient_agentic_inference.reliability import ARMS, reliability_summary

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--runs", type=Path, required=True, help="ARM/predictions and ARM/evaluation")
parser.add_argument("--split", type=Path, default=Path("splits/validation-v1.json"))
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
campaign = json.loads(Path("configs/reliability-validation-v1.json").read_text())
if digest(args.split.read_bytes()) != campaign["population"]["sha256"]:
    parser.error("Split differs from preregistration")
split = json.loads(args.split.read_text())
repositories = {row["instance_id"]: row["repo"] for row in split["instances"]}
if len(repositories) != campaign["population"]["selected"]:
    parser.error("Unexpected selected population")
metrics, identities = {}, {}
reference = None
for arm in ARMS:
    prediction_dir, evaluation_dir = (
        args.runs / arm / name for name in ("predictions", "evaluation")
    )
    verify_artifacts(prediction_dir)
    verify_artifacts(evaluation_dir)
    predictions = read_jsonl(prediction_dir / "predictions.jsonl")
    summary = json.loads((evaluation_dir / "summary.json").read_text())
    manifest = json.loads((prediction_dir / "manifest.json").read_text())
    prediction_hash = digest((prediction_dir / "predictions.jsonl").read_bytes())
    if summary["predictions_sha256"] != prediction_hash:
        parser.error("Evaluation does not reference the supplied predictions")
    base = json.loads(Path(campaign["arms"][arm]).read_text())
    for key in ("model", "artifact", "prompt", "decoding"):
        if manifest[key] != base[key]:
            parser.error(f"{arm}: {key} differs from preregistration")
    if manifest.get("output_constraint") != base.get("output_constraint"):
        parser.error(f"{arm}: output constraint differs from preregistration")
    if manifest["synthetic"] or summary["synthetic"]:
        parser.error("Synthetic artifacts cannot establish validation evidence")
    candidate_identity = {
        p["instance_id"]: (p["candidate_paths"], p["candidate_sha256"]) for p in predictions
    }
    if len(candidate_identity) != len(predictions) or set(candidate_identity) != set(repositories):
        parser.error("Prediction IDs must match the complete split")
    identity = (candidate_identity, summary["gold_sha256"], manifest["inputs_sha256"])
    if reference is not None and identity != reference:
        parser.error("Candidate, gold or input identities differ between arms")
    reference = identity
    metrics[arm] = read_jsonl(evaluation_dir / "metrics.jsonl")
    prediction_by_id = {p["instance_id"]: p for p in predictions}
    for row in metrics[arm]:
        if row["disposition"] != prediction_by_id[row["instance_id"]]["disposition"]:
            parser.error("Metric and prediction dispositions differ")
    identities[arm] = {"predictions_sha256": prediction_hash, "gold_sha256": summary["gold_sha256"]}
result = reliability_summary(metrics, repositories)
result["identities"] = identities
result["campaign_config_sha256"] = digest(
    Path("configs/reliability-validation-v1.json").read_bytes()
)
write_artifacts(args.output, {"comparison.json": encoded(result)})
print(json.dumps(result, indent=2))
