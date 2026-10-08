"""Post-hoc descriptive analysis of saved reports; no inference, gold input or repair."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

from efficient_agentic_inference.comparison import paired_comparison

ROOT = Path(__file__).resolve().parents[2]
SOURCES: dict[str, str] = {}


def read(path: Path):
    raw = path.read_bytes()
    SOURCES[path.relative_to(ROOT).as_posix()] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def rows(path: Path):
    raw = path.read_bytes()
    SOURCES[path.relative_to(ROOT).as_posix()] = hashlib.sha256(raw).hexdigest()
    records = [json.loads(line) for line in raw.splitlines()]
    indexed = {r["instance_id"]: r for r in records}
    assert len(indexed) == len(records)
    return indexed


def quality(row):
    return row["all_files"]["recall_at_k"]["5"]


def success(row):
    return row["all_files"]["strict_success_at_k"]["5"] is True


def bounds(metrics):
    values, strict = [], 0
    for row in metrics.values():
        m = row["all_files"]
        n = m["gold_file_count"]
        assert n > 0
        count = m["candidate_recall_ceiling"] * n
        assert math.isclose(count, round(count), abs_tol=1e-8)
        available = round(count)
        values.append(min(5, available) / n)
        strict += available == n and n <= 5
    return {
        "selected": len(metrics),
        "candidate_recall_ceiling": sum(
            r["all_files"]["candidate_recall_ceiling"] for r in metrics.values()
        )
        / len(metrics),
        "ideal_candidate_top5_recall": sum(values) / len(values),
        "ideal_candidate_top5_strict": strict,
        "scope": (
            "Evaluator-only upper bound; does not establish sufficient excerpts "
            "or an achievable ranker"
        ),
    }


def model_pair(folder, small, large, split):
    base = ROOT / "results/reports" / folder
    left = rows(base / small / "evaluation/metrics.jsonl")
    right = rows(base / large / "evaluation/metrics.jsonl")
    repos = {r["instance_id"]: r["repo"] for r in read(ROOT / "splits" / split)["instances"]}
    result = paired_comparison(list(right.values()), list(left.values()), repos)
    result.pop("decision_rule_pass")  # No post-hoc acceptance rule.
    result["limitation"] = (
        "POST_HOC descriptive contrast; not a new preregistered finding or equivalence test"
    )
    categories = {"both_strict_success": 0, "small_only": 0, "large_only": 0, "neither": 0}
    for key in left:
        a, b = success(left[key]), success(right[key])
        category = (
            "both_strict_success"
            if a and b
            else "small_only"
            if a
            else "large_only"
            if b
            else "neither"
        )
        categories[category] += 1
    result["strict_complementarity"] = categories
    result["perfect_output_choice_strict"] = len(left) - categories["neither"]
    result["perfect_output_choice_recall"] = sum(
        max(quality(left[k]), quality(right[k])) for k in left
    ) / len(left)
    result["oracle_scope"] = (
        "Perfect evaluator-aware choice between saved outputs; not an implemented "
        "fallback/router, merged ranking or measured economics"
    )
    result["candidate_bounds"] = bounds(left)
    result["small_mean_recall5"] = sum(map(quality, left.values())) / len(left)
    result["small_gap_to_ideal_candidate_top5"] = (
        result["candidate_bounds"]["ideal_candidate_top5_recall"] - result["small_mean_recall5"]
    )
    return result


def score_decomposition(model):
    base = ROOT / "results/reports/score-ranking-validation-v2-l4"
    paths = rows(base / (model + "-paths") / "evaluation/metrics.jsonl")
    scores = rows(base / (model + "-scores") / "evaluation/metrics.jsonl")
    predictions = rows(base / (model + "-scores") / "predictions/predictions.jsonl")
    repos = {
        r["instance_id"]: r["repo"] for r in read(ROOT / "splits/validation-v2.json")["instances"]
    }
    groups = defaultdict(lambda: {"tasks": 0, "sum_recall5_difference": 0.0})
    by_repo = defaultdict(lambda: {"tasks": 0, "sum_recall5_difference": 0.0})
    for key in paths:
        delta = quality(scores[key]) - quality(paths[key])
        kind = (
            "empty_score_ranking"
            if not predictions[key]["ranked_files"]
            else "nonempty_score_ranking"
        )
        for group in (groups[kind], by_repo[repos[key]]):
            group["tasks"] += 1
            group["sum_recall5_difference"] += delta
    for group in [*groups.values(), *by_repo.values()]:
        group["contribution_to_all_task_difference"] = group["sum_recall5_difference"] / len(paths)
        group["mean_within_group_difference"] = group["sum_recall5_difference"] / group["tasks"]
    return {
        "status": "POST_HOC_DESCRIPTIVE; selected output groups are not causal evidence",
        "by_empty_ranking": dict(groups),
        "by_repository": dict(by_repo),
    }


def main():
    # Check immutable report envelopes before deriving any new summaries.
    verified = {}
    for folder in (
        "untuned-dev-v2-l4",
        "generalist-dev-v2-l4",
        "reliability-validation-v1-l4",
        "score-ranking-validation-v2-l4",
    ):
        base = ROOT / "results/reports" / folder
        sums = base / "SHA256SUMS"
        SOURCES[sums.relative_to(ROOT).as_posix()] = hashlib.sha256(sums.read_bytes()).hexdigest()
        count = 0
        for line in sums.read_text().splitlines():
            expected, relative = line.split("  ", 1)
            assert hashlib.sha256((base / relative).read_bytes()).hexdigest() == expected, relative
            count += 1
        verified[folder] = count
    result = {
        "status": (
            "POST_HOC_DESCRIPTIVE; not preregistration, inference, training or an economic result"
        ),
        "date": "2026-10-08",
        "report_checksums_verified": verified,
        "cross_model_pairs": {
            "dev-v2_unconstrained": model_pair(
                "generalist-dev-v2-l4",
                "small-replication-dev-v2",
                "generalist-dev-v2",
                "dev-v2.json",
            ),
            "validation-v1_constrained": model_pair(
                "reliability-validation-v1-l4",
                "S-constrained",
                "G-constrained",
                "validation-v1.json",
            ),
            "validation-v2_paths": model_pair(
                "score-ranking-validation-v2-l4", "S-paths", "G-paths", "validation-v2.json"
            ),
        },
        "score_loss_decomposition": {m: score_decomposition(m) for m in ("S", "G")},
        "source_sha256": SOURCES,
    }
    result["analysis_script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target = ROOT / "docs/technical-reports/localization-synthesis-analysis.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
