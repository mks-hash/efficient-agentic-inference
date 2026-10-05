"""Strict canonical inputs, deterministic lexical ranking and file metrics."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import PurePosixPath

KS = (1, 3, 5, 10)


def valid_path(path: object) -> bool:
    if not isinstance(path, str) or not path or "\\" in path or "\0" in path:
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
class InferenceInstance:
    instance_id: str
    repository: str
    base_commit: str
    issue: str
    candidates: tuple[Candidate, ...]

    @classmethod
    def from_record(cls, record: dict) -> InferenceInstance:
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


@dataclass(frozen=True)
class PreparedInference:
    """Inference-only preparation envelope. No upstream record is retained."""

    instance: InferenceInstance
    preparation_status: str
    failure_reason: str | None
    tree_sha256: str | None
    candidate_sha256: str

    @classmethod
    def from_record(cls, record: dict) -> PreparedInference:
        fields = {
            "schema_version",
            "instance",
            "preparation_status",
            "failure_reason",
            "tree_sha256",
            "candidate_sha256",
        }
        if not isinstance(record, dict) or set(record) != fields:
            raise ValueError("Unexpected inference envelope fields")
        if record["schema_version"] != "2.0.0":
            raise ValueError("Unsupported inference schema")
        instance = InferenceInstance.from_record(record["instance"])
        if record["failure_reason"] is not None and (
            not isinstance(record["failure_reason"], str) or not record["failure_reason"]
        ):
            raise ValueError("Failure reason must be null or a nonempty string")
        if record["preparation_status"] == "prepared" and (
            record["failure_reason"] is not None
            or not isinstance(record["tree_sha256"], str)
            or not re.fullmatch(r"[a-f0-9]{64}", record["tree_sha256"])
        ):
            raise ValueError("Prepared inference must have a tree checksum and no failure reason")
        if record["preparation_status"] not in {"prepared", "failed_checkout", "parse_failure"}:
            raise ValueError("Invalid preparation status")
        from .records import digest, encoded

        candidates = [{"path": c.path, "text": c.text} for c in instance.candidates]
        if digest(encoded(candidates)) != record["candidate_sha256"]:
            raise ValueError("Candidate checksum mismatch")
        if record["preparation_status"] != "prepared" and (
            instance.candidates or not record["failure_reason"]
        ):
            raise ValueError("Failed preparation must have no candidates and a reason")
        return cls(
            instance,
            record["preparation_status"],
            record["failure_reason"],
            record["tree_sha256"],
            record["candidate_sha256"],
        )


def rank_files(task: InferenceInstance, limit: int = 10) -> list[str]:
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
