"""Evaluation-only labels. Git parses paths; strict metadata identifies old paths."""

from __future__ import annotations

import ast
import re
import subprocess
from dataclasses import dataclass

from .inference import valid_path


@dataclass(frozen=True)
class EvaluationInstance:
    instance_id: str
    label_status: str
    failure_reason: str | None
    changes: tuple[dict, ...]

    def to_record(self) -> dict:
        return {
            "schema_version": "2.0.0",
            "instance_id": self.instance_id,
            "label_status": self.label_status,
            "failure_reason": self.failure_reason,
            "changes": list(self.changes),
        }

    @classmethod
    def from_record(cls, record: dict) -> EvaluationInstance:
        if not isinstance(record, dict):
            raise ValueError("Evaluation record must be an object")
        if (
            set(record)
            != {"schema_version", "instance_id", "label_status", "failure_reason", "changes"}
            or record["schema_version"] != "2.0.0"
        ):
            raise ValueError("Invalid evaluation record")
        if record["label_status"] not in {
            "labeled",
            "empty_patch",
            "unsupported_patch",
            "parse_failure",
        }:
            raise ValueError("Invalid label status")
        seen = set()
        if not isinstance(record["instance_id"], str) or not record["instance_id"]:
            raise ValueError("Invalid evaluation instance ID")
        if not isinstance(record["changes"], list):
            raise ValueError("Changes must be an array")
        if record["label_status"] == "labeled" and not record["changes"]:
            raise ValueError("Labeled record must have changes")
        if record["label_status"] != "labeled" and record["changes"]:
            raise ValueError("Unlabeled record must not contain guessed changes")
        if record["label_status"] in {"unsupported_patch", "parse_failure"} and (
            not isinstance(record["failure_reason"], str) or not record["failure_reason"]
        ):
            raise ValueError("Label failure needs a reason")
        for change in record["changes"]:
            if not isinstance(change, dict):
                raise ValueError("Change must be an object")
            if set(change) != {"path", "old_path", "new_path", "status", "category", "binary"}:
                raise ValueError("Invalid change fields")
            if not valid_path(change["path"]) or change["path"] in seen:
                raise ValueError("Invalid or duplicate label path")
            if any(
                p is not None and not valid_path(p)
                for p in (change["old_path"], change["new_path"])
            ):
                raise ValueError("Invalid old/new paths")
            if change["category"] not in {"implementation", "test", "non_code"}:
                raise ValueError("Invalid label category")
            if change["status"] not in {
                "modified",
                "added",
                "deleted",
                "renamed",
                "copied",
                "mode_changed",
            }:
                raise ValueError("Invalid change status")
            if not isinstance(change["binary"], bool):
                raise ValueError("Binary indicator must be boolean")
            seen.add(change["path"])
        return cls(
            record["instance_id"],
            record["label_status"],
            record["failure_reason"],
            tuple(record["changes"]),
        )


def category(path: str) -> str:
    parts = path.split("/")
    if any(p in {"test", "tests", "testing"} for p in parts[:-1]) or parts[-1].startswith("test_"):
        return "test"
    return "implementation" if path.endswith(".py") else "non_code"


def unquote_path(value: str) -> str:
    if value.startswith('"'):
        return ast.literal_eval("b" + value).decode("utf-8")
    return value


def labels(instance_id: str, patch: str) -> EvaluationInstance:
    if not patch.strip():
        return EvaluationInstance(instance_id, "empty_patch", "No solution patch", ())
    parsed = subprocess.run(
        ["git", "apply", "--numstat", "-z"], input=patch.encode(), capture_output=True, check=False
    )
    if parsed.returncode:
        return EvaluationInstance(instance_id, "parse_failure", parsed.stderr.decode().strip(), ())
    try:
        stats = [item.split(b"\t", 2) for item in parsed.stdout.split(b"\0") if item]
        blocks = re.split(r"(?m)^diff --git ", patch)[1:]
        if not blocks or len(stats) != len(blocks):
            raise ValueError("Unsupported diff structure or stats count")
        changes = []
        for stat, block in zip(stats, blocks, strict=True):
            target = stat[2].decode("utf-8")
            header = block.split("\n@@", 1)[0]
            meta = header.splitlines()[1:]
            status, old, new = "modified", target, target
            if any(line.startswith("new file mode ") for line in meta):
                status, old = "added", None
            elif any(line.startswith("deleted file mode ") for line in meta):
                status, new = "deleted", None
            elif any(line.startswith("rename from ") for line in meta):
                status = "renamed"
                old = unquote_path(
                    next(line[12:] for line in meta if line.startswith("rename from "))
                )
            elif any(line.startswith("copy from ") for line in meta):
                status, old = "copied", None
            elif not any(line.startswith("--- ") for line in meta):
                status = "mode_changed"
            path = old if old is not None else new
            if not valid_path(path) or any(p is not None and not valid_path(p) for p in (old, new)):
                raise ValueError("Unsafe or unsupported diff path")
            changes.append(
                {
                    "path": path,
                    "old_path": old,
                    "new_path": new,
                    "status": status,
                    "category": category(path),
                    "binary": b"-" in stat[:2]
                    or "GIT binary patch" in header
                    or "Binary files " in header,
                }
            )
        if len({c["path"] for c in changes}) != len(changes):
            raise ValueError("Duplicate paths across diff sections")
        return EvaluationInstance(instance_id, "labeled", None, tuple(changes))
    except (ValueError, SyntaxError, UnicodeError, IndexError) as exc:
        return EvaluationInstance(instance_id, "unsupported_patch", str(exc), ())
