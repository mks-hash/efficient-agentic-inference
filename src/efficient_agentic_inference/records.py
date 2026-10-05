"""Canonical byte encoding and immutable artifact I/O; no dataset/evaluation imports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, indent=2) + "\n").encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def jsonl(records: list[dict]) -> bytes:
    return b"".join(
        (json.dumps(record, sort_keys=True, ensure_ascii=True) + "\n").encode()
        for record in records
    )


def write_artifacts(output: Path, artifacts: dict[str, bytes]) -> None:
    output.mkdir(parents=True, exist_ok=False)
    for name, data in artifacts.items():
        (output / name).write_bytes(data)
    (output / "checksums.json").write_bytes(
        encoded({name: digest(data) for name, data in artifacts.items()})
    )


def verify_artifacts(folder: Path) -> dict:
    checksums = json.loads((folder / "checksums.json").read_text())
    for name, expected in checksums.items():
        if Path(name).name != name or digest((folder / name).read_bytes()) != expected:
            raise ValueError(f"Artifact checksum mismatch: {name}")
    return checksums
