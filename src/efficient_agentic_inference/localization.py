"""Strict canonical inputs, deterministic lexical ranking and file metrics."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import PurePosixPath

KS = (1, 3, 5, 10)


def valid_path(path: object) -> bool:
    if not isinstance(path, str) or not path or "\\" in path:
        return False
    return not PurePosixPath(path).is_absolute() and all(
        part not in {"", ".", ".."} for part in path.split("/")
    )


def tokens(text: str) -> list[str]:
    """Split identifiers too, so file_path is searchable as file + path."""
    return re.findall(r"[a-z0-9]+", text.lower())


@dataclass(frozen=True)
class Candidate:
    path: str
    text: str


@dataclass(frozen=True)
class Task:
    instance_id: str
    repository: str
    base_commit: str
    issue: str
    candidates: tuple[Candidate, ...]

    @classmethod
    def from_record(cls, record: dict) -> Task:
        expected = {"instance_id", "repository", "base_commit", "issue", "candidates"}
        if not isinstance(record, dict) or set(record) != expected:
            raise ValueError("Task fields must match canonical input; no gold/extra metadata")
        for name in expected - {"candidates"}:
            if not isinstance(record[name], str) or not record[name].strip():
                raise ValueError(f"Task {name} must be a nonempty string")
        if not isinstance(record["candidates"], list):
            raise ValueError("candidates must be an array")
        candidates = []
        for item in record["candidates"]:
            if not isinstance(item, dict) or set(item) != {"path", "text"}:
                raise ValueError("Candidate must have exactly path and text")
            if not valid_path(item["path"]) or not isinstance(item["text"], str):
                raise ValueError("Invalid candidate path or text")
            candidates.append(Candidate(**item))
        if len({c.path for c in candidates}) != len(candidates):
            raise ValueError("Duplicate candidate paths")
        return cls(**{**record, "candidates": tuple(candidates)})


def rank_files(task: Task, limit: int = 10) -> list[str]:
    """BM25 over supplied candidate path + text, with path-sorted ties.

    This ranks the supplied corpus only: it does not implement repository retrieval.
    k1=1.2 and b=0.75 are fixed in lexical-bm25-v1, without gold-informed tuning.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    if not task.candidates:
        return []
    docs = [Counter(tokens(c.path + " " + c.text)) for c in task.candidates]
    lengths = [sum(doc.values()) for doc in docs]
    average = sum(lengths) / len(docs) or 1.0
    query = set(tokens(task.issue))
    frequencies = {word: sum(word in doc for doc in docs) for word in query}
    scored = []
    for candidate, doc, length in zip(task.candidates, docs, lengths, strict=True):
        score = 0.0
        for word in sorted(query):
            tf = doc[word]
            if not tf:
                continue
            df = frequencies[word]
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            denominator = tf + 1.2 * (1 - 0.75 + 0.75 * length / average)
            score += idf * tf * 2.2 / denominator
        scored.append((score, candidate.path))
    return [path for _, path in sorted(scored, key=lambda pair: (-pair[0], pair[1]))[:limit]]


def prediction_error(ranked: object, candidates: set[str]) -> str | None:
    if not isinstance(ranked, list) or any(not valid_path(path) for path in ranked):
        return "Prediction must be an array of repository-relative paths"
    if len(set(ranked)) != len(ranked):
        return "Prediction contains duplicate paths"
    if not set(ranked) <= candidates:
        return "Prediction contains unknown candidate paths"
    return None


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
