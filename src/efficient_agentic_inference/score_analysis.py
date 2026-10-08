"""Score-recipe comparison; reuse the frozen paired statistical/validity rule."""

from __future__ import annotations

from .reliability import reliability_summary

ARMS = ("S-paths", "S-scores", "G-paths", "G-scores")


def score_summary(arms: dict[str, list[dict]], repositories: dict[str, str]) -> dict:
    if set(arms) != set(ARMS):
        raise ValueError("Exactly four score-campaign arms are required")
    # Reuse the already specified paired calculation, not historical predictions.
    # These aliases are internal; both actual recipes use generation constraints.
    translated = {
        f"{model}-{old}": arms[f"{model}-{new}"]
        for model in ("S", "G")
        for old, new in (("free", "paths"), ("constrained", "scores"))
    }
    result = reliability_summary(translated, repositories)
    result["contract"] = "score-ranking-validation-v2"
    result["intervention"] = "Entire prompt / score representation / deterministic mapping recipe"
    for model, contrast in result["contrasts"].items():
        contrast["contrast"] = [f"{model}-scores", f"{model}-paths"]
        contrast["valid_paths"] = contrast.pop("valid_free")
        contrast["valid_scores"] = contrast.pop("valid_constrained")
        discordance = contrast["validity_discordance"]
        contrast["validity_discordance"] = {
            "paths_invalid_scores_valid": discordance["free_invalid_constrained_valid"],
            "paths_valid_scores_invalid": discordance["free_valid_constrained_invalid"],
        }
    result["limitation"] = (
        "Thirty new issues in four seen repositories; whole recipe, not uniqueness alone. "
        "Numerical signal requires independent technical/provenance gates. "
        "No equivalence, training, generalization or economic claim follows."
    )
    return result
