#!/usr/bin/env python3
"""Freeze score-campaign sources/configs before validation reconstruction."""

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from efficient_agentic_inference.records import digest, encoded, write_artifacts
from efficient_agentic_inference.score_analysis import ARMS

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
campaign_path = Path("configs/score-ranking-validation-v2.json")
campaign = json.loads(campaign_path.read_text())
split = Path(campaign["population"]["split"])
if digest(split.read_bytes()) != campaign["population"]["sha256"]:
    parser.error("Validation split checksum mismatch")
if len(json.loads(split.read_text())["instances"]) != campaign["population"]["selected"]:
    parser.error("Unexpected population size")
if set(campaign["arms"]) != set(ARMS) or campaign["arm_order"] != [
    "S-paths",
    "S-scores",
    "G-scores",
    "G-paths",
]:
    parser.error("Arms/order differ from preregistration")
configs = {arm: json.loads(Path(path).read_text()) for arm, path in campaign["arms"].items()}
for arm, config in configs.items():
    prompt = Path(config["prompt"]["system_file"])
    if digest(prompt.read_bytes()) != config["prompt"]["sha256"]:
        parser.error(f"{arm}: prompt checksum mismatch")
    if config["population"] != {key: campaign["population"][key] for key in ("split", "sha256")}:
        parser.error(f"{arm}: population mismatch")
for model in ("S", "G"):
    paired = []
    for mode, policy, system in (
        ("paths", "candidate-json-array-v1", "configs/prompts/localization-v1.txt"),
        ("scores", "candidate-score-vector-v1", "configs/prompts/candidate-scores-v1.txt"),
    ):
        config = dict(configs[f"{model}-{mode}"])
        if config.pop("output_constraint") != {"policy": policy}:
            parser.error("Constraint differs from preregistration")
        prompt = config.pop("prompt")
        if prompt["system_file"] != system:
            parser.error("Unexpected prompt path")
        config.pop("campaign")
        paired.append(config)
    if paired[0] != paired[1]:
        parser.error("Within-model configs differ beyond campaign/prompt/constraint")
files = [
    campaign_path,
    split,
    Path("configs/prompts/localization-v1.txt"),
    Path("configs/prompts/candidate-scores-v1.txt"),
    Path("decisions/0009-score-vector-ranking.md"),
    Path("docs/experiments/score-ranking-validation-v2.md"),
    Path("docs/benchmark-localization-v2.md"),
    Path("docs/cost-accounting-v1.md"),
    *(Path(path) for path in campaign["arms"].values()),
    *(
        Path("tools") / name
        for name in (
            "freeze-score-ranking.py",
            "analyze-score-ranking.py",
            "configure-cpu-run.py",
            "llama-isolated.sh",
        )
    ),
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
            "score_analysis.py",
            "evaluation.py",
            "metrics.py",
            "labeler.py",
            "snapshot.py",
            "localization.py",
        )
    ),
]
contents = {path.as_posix(): path.read_bytes() for path in files}
freeze = {
    "contract": campaign["contract"],
    "frozen_at_utc": datetime.now(UTC).isoformat(),
    "files": {name: digest(data) for name, data in contents.items()},
    "code_identity": {
        "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
    },
    "role": "Preparation snapshot before reconstruction; not execution freeze",
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
