"""Paired repository-block uncertainty from completed evaluation records only."""

from __future__ import annotations

import math
import random


def paired_comparison(model: list[dict], control: list[dict], repositories: dict[str, str]) -> dict:
    def indexed(rows):
        by_id = {r["instance_id"]: r for r in rows}
        if not rows or len(by_id) != len(rows):
            raise ValueError("Metrics must have unique, nonempty IDs")
        return by_id

    model_by_id, control_by_id = indexed(model), indexed(control)
    if set(model_by_id) != set(control_by_id) or set(model_by_id) != set(repositories):
        raise ValueError("Paired metrics and repository membership must match exactly")
    groups: dict[str, list[float]] = {}
    strict_model = strict_control = 0
    for instance_id in sorted(model_by_id):
        left, right = (rows[instance_id]["all_files"] for rows in (model_by_id, control_by_id))
        scores = [left["recall_at_k"]["5"], right["recall_at_k"]["5"]]
        if any(v is None for v in scores):
            raise ValueError("Primary paired analysis requires defined recall for every task")
        if left["gold_file_count"] != right["gold_file_count"]:
            raise ValueError("Gold count mismatch")
        if left["candidate_recall_ceiling"] != right["candidate_recall_ceiling"]:
            raise ValueError("Matched candidate ceiling mismatch")
        groups.setdefault(repositories[instance_id], []).append(scores[0] - scores[1])
        strict_model += left["strict_success_at_k"]["5"] is True
        strict_control += right["strict_success_at_k"]["5"] is True
    names = sorted(groups)
    rng = random.Random(20261006)
    draws = []
    for _ in range(5000):
        sampled = [v for repo in rng.choices(names, k=len(names)) for v in groups[repo]]
        draws.append(sum(sampled) / len(sampled))
    draws.sort()
    interval = [draws[math.ceil(p * len(draws)) - 1] for p in (0.025, 0.975)]
    gain = sum(sum(g) for g in groups.values()) / len(model)
    return {
        "selected": len(model),
        "repository_blocks": len(groups),
        "recall_at_5_gain": gain,
        "paired_repo_bootstrap_95_ci": interval,
        "strict_model": strict_model,
        "strict_control": strict_control,
        "decision_rule_pass": gain >= 0.05 and strict_model >= strict_control and interval[0] > 0,
        "bootstrap": {
            "resamples": 5000,
            "seed": 20261006,
            "unit": "repository blocks, preserving paired tasks",
            "percentile_method": "nearest-rank",
        },
        "limitation": "Development decision rule; no population-wide or held-out claim",
    }
