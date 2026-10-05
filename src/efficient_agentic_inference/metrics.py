"""Evaluation-only quality and accounting helpers."""

import math

KS = (1, 3, 5, 10)


def evaluate(ranked: list[str], gold: list[str], disposition: str = "valid") -> dict:
    gold_set = set(gold)
    usable = ranked if disposition == "valid" else []
    recall, precision, success = {}, {}, {}
    for k in KS:
        hits = len(set(usable[:k]) & gold_set)
        recall[str(k)] = hits / len(gold_set) if gold_set else None
        precision[str(k)] = hits / k if gold_set else None
        success[str(k)] = bool(gold_set) and gold_set <= set(usable[:k])
    first = next((i for i, path in enumerate(usable, 1) if path in gold_set), None)
    return {
        "recall_at_k": recall,
        "precision_at_k": precision,
        "strict_success_at_k": success,
        "mrr": (1 / first if first else 0.0) if gold_set else None,
        "gold_file_count": len(gold_set),
    }


def summarize(results: list[dict], primary_k: int = 5) -> dict:
    if not results:
        raise ValueError("Cannot summarize an empty run")
    successes = sum(r["metrics"]["strict_success_at_k"][str(primary_k)] for r in results)
    costs = [r["measurements"]["monetary_usd"] for r in results]
    total_cost = sum(costs) if all(c is not None for c in costs) else None
    eligible = [r for r in results if r["metrics"]["gold_file_count"]]
    latencies = sorted(r["measurements"]["wall_ms"] for r in results)
    return {
        "attempted_tasks": len(results),
        "nonempty_gold_tasks": len(eligible),
        "empty_gold_tasks": len(results) - len(eligible),
        "failed_outputs": sum(r["disposition"] != "valid" for r in results),
        "primary_k": primary_k,
        "strict_successes": successes,
        "strict_success_rate": successes / len(results),
        "mean_recall_at_k": {
            str(k): sum(r["metrics"]["recall_at_k"][str(k)] for r in eligible) / len(eligible)
            if eligible
            else None
            for k in KS
        },
        "wall_ms_p50": latencies[math.ceil(0.5 * len(latencies)) - 1],
        "wall_ms_p95": latencies[math.ceil(0.95 * len(latencies)) - 1],
        "quantile_method": "nearest-rank",
        "total_monetary_usd": total_cost,
        "cost_per_success_usd": total_cost / successes
        if total_cost is not None and successes
        else None,
        "cost_per_success_reason": "unknown_cost"
        if total_cost is None
        else ("zero_successes" if not successes else None),
    }
