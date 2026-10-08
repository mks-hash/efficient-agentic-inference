"""Frozen four-arm analysis of completed evaluator records; no inference or repair."""

from __future__ import annotations

from .comparison import paired_comparison

ARMS = ("S-free", "S-constrained", "G-free", "G-constrained")


def reliability_summary(arms: dict[str, list[dict]], repositories: dict[str, str]) -> dict:
    if set(arms) != set(ARMS):
        raise ValueError("Exactly four preregistered arms are required")
    contrasts = {}
    for model in ("S", "G"):
        free, constrained = (arms[f"{model}-{mode}"] for mode in ("free", "constrained"))
        result = paired_comparison(constrained, free, repositories)
        indexed = [{r["instance_id"]: r for r in rows} for rows in (free, constrained)]
        discordance = {"free_invalid_constrained_valid": 0, "free_valid_constrained_invalid": 0}
        valid_free = valid_constrained = 0
        for instance_id in sorted(repositories):
            before, after = (rows[instance_id] for rows in indexed)
            for row in (before, after):
                status = row["disposition"]
                if status not in {"valid", "invalid_output", "runtime_error", "preparation_failed"}:
                    raise ValueError("Unknown prediction disposition")
                metric = row["all_files"]
                if status != "valid" and (
                    metric["recall_at_k"]["5"] != 0
                    or metric["strict_success_at_k"]["5"] is not False
                ):
                    raise ValueError("Failed predictions must retain zero quality")
            old_valid, new_valid = before["disposition"] == "valid", after["disposition"] == "valid"
            valid_free += old_valid
            valid_constrained += new_valid
            discordance["free_invalid_constrained_valid"] += not old_valid and new_valid
            discordance["free_valid_constrained_invalid"] += old_valid and not new_valid
        quality_rule = result.pop("decision_rule_pass")
        result.pop("limitation")
        result.update(
            valid_free=valid_free,
            valid_constrained=valid_constrained,
            validity_discordance=discordance,
            role="primary" if model == "S" else "secondary_exploratory",
        )
        if model == "S":
            result["numerical_signal_rule_pass"] = quality_rule and valid_constrained >= valid_free
        contrasts[model] = result
    # Check cross-model pairing as well, even though only within-model gains are primary.
    paired_comparison(arms["G-free"], arms["S-free"], repositories)
    return {
        "contract": "reliability-validation-v1",
        "contrasts": contrasts,
        "interaction_recall_at_5_point_estimate": contrasts["G"]["recall_at_5_gain"]
        - contrasts["S"]["recall_at_5_gain"],
        "interaction_role": "secondary_exploratory",
        "technical_gates": "NOT_ASSESSED_BY_METRICS",
        "limitation": (
            "Small same-repository validation; numerical signal requires independent technical "
            "and provenance gates. No equivalence, training or economic claim follows."
        ),
    }
