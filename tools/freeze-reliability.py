#!/usr/bin/env python3
"""Freeze the reliability protocol/base configs before validation reconstruction."""

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from efficient_agentic_inference.records import digest, encoded, write_artifacts

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
campaign_path = Path("configs/reliability-validation-v1.json")
campaign = json.loads(campaign_path.read_text())
split = Path(campaign["population"]["split"])
prompt = Path("configs/prompts/localization-v1.txt")
if digest(split.read_bytes()) != campaign["population"]["sha256"]:
    parser.error("Validation split checksum mismatch")
if digest(prompt.read_bytes()) != campaign["prompt_sha256"]:
    parser.error("Prompt checksum mismatch")
configs = {arm: json.loads(Path(path).read_text()) for arm, path in campaign["arms"].items()}
for model in ("S", "G"):
    free, constrained = (dict(configs[f"{model}-{mode}"]) for mode in ("free", "constrained"))
    free.pop("campaign")
    constrained.pop("campaign")
    if "output_constraint" in free:
        parser.error("Free arm must not contain an output constraint")
    if constrained.pop("output_constraint") != {"policy": "candidate-json-array-v1"}:
        parser.error("Constraint differs from preregistration")
    if free != constrained:
        parser.error("Within-model base configs differ beyond campaign and constraint")
files = [
    campaign_path,
    split,
    prompt,
    Path("decisions/0007-constrained-output-validation.md"),
    Path("docs/experiments/reliability-validation-v1.md"),
    *(Path(path) for path in campaign["arms"].values()),
    Path("tools/freeze-reliability.py"),
    Path("tools/analyze-reliability.py"),
    Path("tools/configure-cpu-run.py"),
    Path("tools/llama-isolated.sh"),
    *(
        Path("src/efficient_agentic_inference") / name
        for name in (
            "__init__.py",
            "llama_predict.py",
            "inference.py",
            "records.py",
            "context.py",
            "comparison.py",
            "reliability.py",
            "evaluation.py",
            "metrics.py",
            "labeler.py",
        )
    ),
]
contents = {path.as_posix(): path.read_bytes() for path in files}
freeze = {
    "contract": "reliability-validation-v1",
    "frozen_at_utc": datetime.now(UTC).isoformat(),
    "files": {name: digest(data) for name, data in contents.items()},
    "code_identity": {
        "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
    },
    "role": "Preparation snapshot before validation reconstruction; not execution freeze",
    "validation_inference": "NOT_RUN",
    "paid_execution": "NOT_AUTHORIZED",
}
write_artifacts(
    args.output,
    {
        "freeze.json": encoded(freeze),
        **{name.replace("/", "__"): data for name, data in contents.items()},
    },
)
print(json.dumps({"freeze_sha256": digest(encoded(freeze)), "files": len(contents)}))
