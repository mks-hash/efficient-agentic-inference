"""Render saved paired comparisons; requires Matplotlib 3.10.7, no inference."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "results/reports/untuned-dev-v2-l4"
DESTINATION = Path(__file__).resolve().parent / "figures"


def main() -> None:
    comparisons = [
        ("Matched lexical\nprimary comparison", "paired-comparison.json", "#176b75"),
        (
            "Full-corpus lexical\nsupplementary comparison",
            "full-reference-comparison.json",
            "#687078",
        ),
    ]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(9, 3.8), layout="constrained")
    for row, (_, filename, color) in enumerate(comparisons):
        data = json.loads((REPORT / filename).read_text())
        point = data["recall_at_5_gain"]
        lower, upper = data["paired_repo_bootstrap_95_ci"]
        ax.errorbar(
            point,
            row,
            xerr=[[point - lower], [upper - point]],
            fmt="o",
            markersize=8,
            color=color,
            capsize=6,
            linewidth=2,
        )
        ax.text(0.68, row + 0.28, f"{point:+.4f}  [{lower:+.4f}, {upper:+.4f}]", ha="right")
    ax.axvline(0, color="#a0a0a0", linestyle="--", linewidth=1)
    ax.set_yticks([0, 1], [item[0] for item in comparisons])
    ax.set_ylim(1.6, -0.7)
    ax.set_xlim(-0.05, 0.70)
    ax.set_xlabel("Mean Recall@5 gain: untuned Qwen3-4B minus control")
    ax.set_title("SWE-bench dev-v2 · 60 tasks / 6 repository blocks", loc="left", pad=14)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=0.15)
    DESTINATION.mkdir(parents=True, exist_ok=True)
    fig.savefig(DESTINATION / "untuned-dev-v2-gains.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
