"""Pinned SWE-bench snapshots, deterministic selection and base-tree export."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import urllib.request
from collections import defaultdict
from pathlib import Path

from .inference import InferenceInstance, valid_path
from .labeler import labels
from .records import digest, encoded, jsonl, write_artifacts

ALLOWED_INFERENCE_FIELDS = ("instance_id", "repo", "base_commit", "problem_statement")
POLICY = "python-full-corpus-v1"
MAX_FILE_BYTES = 1024 * 1024


def projection(raw: dict) -> dict:
    return {key: raw[key] for key in ALLOWED_INFERENCE_FIELDS}


def issue_fingerprint(record: dict) -> str:
    return digest(encoded([record["repo"], " ".join(record["problem_statement"].split())]))


def select(
    dev: list[dict], final: list[dict], count: int, seed: str
) -> tuple[list[dict], list[dict]]:
    final_ids = {r["instance_id"] for r in final}
    final_issues = {issue_fingerprint(r) for r in final}
    groups, excluded = defaultdict(list), []
    for raw in dev:
        r = projection(raw)
        if r["instance_id"] in final_ids or issue_fingerprint(r) in final_issues:
            excluded.append({"instance_id": r["instance_id"], "reason": "evaluation_overlap"})
        else:
            groups[r["repo"]].append(r)
    for rows in groups.values():
        rows.sort(key=lambda r: digest((seed + "\0" + r["instance_id"]).encode()))
    selected = []
    while len(selected) < count and any(groups.values()):
        for repo in sorted(groups):
            if groups[repo] and len(selected) < count:
                selected.append(groups[repo].pop(0))
    if len(selected) != count or count < 1:
        raise ValueError("Insufficient eligible tasks for requested sample")
    if len({r["instance_id"] for r in selected}) != len(selected):
        raise ValueError("Duplicate selected instance IDs")
    return selected, excluded


def download_sources(config: Path, output: Path) -> None:
    config_record = json.loads(config.read_text())
    output.mkdir(parents=True, exist_ok=True)
    for source in config_record["sources"]:
        path = output / source["local_name"]
        if path.exists() and digest(path.read_bytes()) == source["sha256"]:
            continue
        with urllib.request.urlopen(source["url"], timeout=90) as response:
            payload = response.read()
        if digest(payload) != source["sha256"]:
            raise ValueError("Upstream file checksum mismatch")
        path.write_bytes(payload)


def verify_sources(config: Path, folder: Path) -> dict:
    result = json.loads(config.read_text())
    for source in result["sources"]:
        if digest((folder / source["local_name"]).read_bytes()) != source["sha256"]:
            raise ValueError("Pinned dataset checksum mismatch")
    return result


def freeze_splits(config: Path, upstream: Path, output: Path, count: int, seed: str) -> None:
    import pyarrow.parquet as pq

    sources = verify_sources(config, upstream)
    # Selection never reads patches, labels, difficulty, hints or test metadata.
    dev = pq.read_table(
        upstream / "dev.parquet", columns=list(ALLOWED_INFERENCE_FIELDS)
    ).to_pylist()
    final = pq.read_table(
        upstream / "verified.parquet", columns=list(ALLOWED_INFERENCE_FIELDS)
    ).to_pylist()
    selected, excluded = select(dev, final, count, seed)
    dev_manifest = {
        "schema_version": "1.0.0",
        "name": "dev-v1",
        "sources": sources,
        "selection": {"algorithm": "repo-round-robin-sha256-v1", "count": count, "seed": seed},
        "source_population": len(dev),
        "overlap_exclusions": excluded,
        "instances": [
            {
                "instance_id": r["instance_id"],
                "repo": r["repo"],
                "base_commit": r["base_commit"],
                "issue_sha256": issue_fingerprint(r),
            }
            for r in selected
        ],
    }
    evaluation_manifest = {
        "schema_version": "1.0.0",
        "name": "evaluation-v1",
        "sources": sources,
        "instance_ids": sorted(r["instance_id"] for r in final),
        "status": "reserved; no final predictions or labels produced",
    }
    write_artifacts(
        output,
        {"dev-v1.json": encoded(dev_manifest), "evaluation-v1.json": encoded(evaluation_manifest)},
    )


def git(cache: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "--git-dir", str(cache), *args], check=True, capture_output=True, timeout=180
    ).stdout


def export_base(repo: str, commit: str, cache_root: Path, output: Path, offline: bool) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Invalid GitHub repository identity")
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("Base commit must be a full SHA")
    cache = cache_root / repo.replace("/", "__")
    if not cache.exists():
        if offline:
            raise ValueError("Missing offline Git object cache")
        cache.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "--bare", str(cache)], check=True, capture_output=True)
    try:
        git(cache, "cat-file", "-e", commit + "^{commit}")
    except subprocess.CalledProcessError:
        if offline:
            raise ValueError("Missing offline base commit") from None
        git(cache, "fetch", "--depth=1", "--no-tags", "https://github.com/" + repo + ".git", commit)
    resolved = git(cache, "rev-parse", commit + "^{commit}").decode().strip()
    if resolved != commit:
        raise ValueError("Base commit identity mismatch")
    git_tree = git(cache, "rev-parse", commit + "^{tree}").decode().strip()
    # Read Git blobs directly: archive attributes (export-ignore/export-subst)
    # must not remove or rewrite evidence from the actual base tree.
    tracked = []
    for item in git(cache, "ls-tree", "-r", "-z", commit).split(b"\0"):
        if not item:
            continue
        metadata, raw_path = item.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = raw_path.decode("utf-8")
        if not valid_path(path) or ".git" in path.split("/"):
            raise ValueError("Unsafe Git tree path")
        tracked.append((path, mode, kind, oid))
    object_ids = sorted({oid for _, _, kind, oid in tracked if kind == "blob"})
    process = subprocess.run(
        ["git", "--git-dir", str(cache), "cat-file", "--batch"],
        input=("\n".join(object_ids) + "\n").encode(),
        check=True,
        capture_output=True,
        timeout=180,
    )
    stream = io.BytesIO(process.stdout)
    blobs = {}
    for expected in object_ids:
        oid, kind, size = stream.readline().decode().strip().split()
        payload = stream.read(int(size))
        if stream.read(1) != b"\n" or oid != expected or kind != "blob":
            raise ValueError("Git blob framing mismatch")
        computed = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
        if computed != oid:
            raise ValueError("Git blob identity mismatch")
        blobs[oid] = payload
    entries = []
    output.mkdir(parents=True, exist_ok=False)
    for name, mode, object_kind, oid in tracked:
        if object_kind == "commit":
            payload, kind = oid.encode(), "submodule_not_expanded"
        elif mode == "120000":
            payload, kind = blobs[oid], "symlink_not_materialized"
        elif mode in {"100644", "100755"}:
            payload, kind = blobs[oid], "regular"
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        else:
            raise ValueError("Unsupported Git tree entry")
        entries.append(
            {
                "path": name,
                "size": len(payload),
                "content_sha256": digest(payload),
                "kind": kind,
                "mode": mode,
                "git_object": oid,
            }
        )
    return {
        "repo": repo,
        "base_commit": commit,
        "git_tree": git_tree,
        "files": sorted(entries, key=lambda e: e["path"]),
        "policy": "exact Git blobs; symlinks recorded, not followed; submodules not expanded",
    }


def inference_record(allowed: dict, tree: Path, tree_manifest: dict) -> tuple[dict, dict]:
    if set(allowed) != set(ALLOWED_INFERENCE_FIELDS):
        raise ValueError("Candidate builder accepts only inference projection")
    candidates, candidate_manifest = [], []
    for entry in tree_manifest["files"]:
        disposition = "included"
        if entry["kind"] != "regular":
            disposition = "non_regular"
        elif not entry["path"].endswith(".py"):
            disposition = "non_python"
        elif entry["size"] > MAX_FILE_BYTES:
            disposition = "file_size_limit"
        else:
            payload = (tree / entry["path"]).read_bytes()
            if digest(payload) != entry["content_sha256"]:
                raise ValueError("Base file checksum mismatch")
            try:
                text = payload.decode("utf-8")
                if "\0" in text:
                    raise UnicodeError("NUL in candidate")
                candidates.append({"path": entry["path"], "text": text})
            except UnicodeError:
                disposition = "non_utf8_or_binary"
        candidate_manifest.append(
            {
                "path": entry["path"],
                "disposition": disposition,
                "content_sha256": entry["content_sha256"],
            }
        )
    candidates.sort(key=lambda c: c["path"])
    instance = {
        "instance_id": allowed["instance_id"],
        "repository": allowed["repo"],
        "base_commit": allowed["base_commit"],
        "issue": allowed["problem_statement"],
        "candidates": candidates,
    }
    InferenceInstance.from_record(instance)
    record = {
        "schema_version": "2.0.0",
        "instance": instance,
        "preparation_status": "prepared",
        "failure_reason": None,
        "tree_sha256": digest(encoded(tree_manifest)),
        "candidate_sha256": digest(encoded(candidates)),
    }
    return record, {
        "policy": POLICY,
        "max_file_bytes": MAX_FILE_BYTES,
        "files": candidate_manifest,
        "candidate_sha256": record["candidate_sha256"],
    }


def build(
    config: Path, upstream: Path, split: Path, output: Path, cache: Path, offline: bool
) -> dict:
    import pyarrow.parquet as pq

    sources = verify_sources(config, upstream)
    selection = json.loads(split.read_text())
    if selection["sources"] != sources:
        raise ValueError("Split source identity differs from pinned sources")
    if output.exists():
        raise ValueError("Snapshot exists; cannot overwrite")
    raw_rows = pq.read_table(upstream / "dev.parquet").to_pylist()
    rows = {r["instance_id"]: r for r in raw_rows}
    if len(rows) != len(raw_rows):
        raise ValueError("Duplicate upstream instance IDs")
    inputs, gold, population = [], [], []
    output.mkdir(parents=True)
    (output / "repos").mkdir()
    for selected in selection["instances"]:
        raw = rows[selected["instance_id"]]
        allowed = projection(raw)
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", allowed["instance_id"]):
            raise ValueError("Unsafe instance ID for export directory")
        if (
            allowed["base_commit"] != selected["base_commit"]
            or allowed["repo"] != selected["repo"]
            or issue_fingerprint(allowed) != selected["issue_sha256"]
        ):
            raise ValueError("Selected task identity mismatch")
        folder = output / "repos" / allowed["instance_id"]
        preparation_stage = "failed_checkout"
        try:
            tree = export_base(
                allowed["repo"], allowed["base_commit"], cache, folder / "tree", offline
            )
            preparation_stage = "parse_failure"
            record, candidates = inference_record(allowed, folder / "tree", tree)
            (folder / "TREE_MANIFEST.json").write_bytes(encoded(tree))
            (folder / "CANDIDATE_MANIFEST.json").write_bytes(encoded(candidates))
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            record = {
                "schema_version": "2.0.0",
                "instance": {
                    "instance_id": allowed["instance_id"],
                    "repository": allowed["repo"],
                    "base_commit": allowed["base_commit"],
                    "issue": allowed["problem_statement"],
                    "candidates": [],
                },
                "preparation_status": preparation_stage,
                "failure_reason": f"{type(exc).__name__}: {exc}",
                "tree_sha256": None,
                "candidate_sha256": digest(encoded([])),
            }
        inputs.append(record)  # Frozen before label derivation; never altered based on gold.
        evaluation = labels(allowed["instance_id"], raw["patch"])
        gold.append(evaluation.to_record())
        population.append(
            {
                "instance_id": allowed["instance_id"],
                "preparation_status": record["preparation_status"],
                "preparation_reason": record["failure_reason"],
                "label_status": evaluation.label_status,
                "label_reason": evaluation.failure_reason,
            }
        )
        print(
            f"{allowed['instance_id']}: {record['preparation_status']}, {evaluation.label_status}",
            flush=True,
        )
    write_artifacts(output / "inference_inputs", {"tasks.jsonl": jsonl(inputs)})
    write_artifacts(output / "gold", {"labels.jsonl": jsonl(gold)})
    manifest = {
        "schema_version": "2.0.0",
        "contract": "localization-v2",
        "sources": sources,
        "split_sha256": digest(split.read_bytes()),
        "candidate_policy": POLICY,
        "label_policy": "solution-patch-files-v2",
        "population": population,
        "inputs_sha256": digest(jsonl(inputs)),
        "gold_sha256": digest(jsonl(gold)),
        "selected": len(population),
        "prepared": sum(p["preparation_status"] == "prepared" for p in population),
        "labeled": sum(p["label_status"] == "labeled" for p in population),
    }
    (output / "snapshot.json").write_bytes(encoded(manifest))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("--config", type=Path, required=True)
    fetch.add_argument("--output", type=Path, required=True)
    freeze = sub.add_parser("freeze")
    prepare = sub.add_parser("build")
    for p in (freeze, prepare):
        p.add_argument("--config", type=Path, required=True)
        p.add_argument("--upstream", type=Path, required=True)
        p.add_argument("--output", type=Path, required=True)
    freeze.add_argument("--count", type=int, default=12)
    freeze.add_argument("--seed", default="eai-dev-v1")
    prepare.add_argument("--split", type=Path, required=True)
    prepare.add_argument("--cache", type=Path, required=True)
    prepare.add_argument("--offline", action="store_true")
    args = vars(parser.parse_args())
    command = args.pop("command")
    try:
        if command == "fetch":
            download_sources(**args)
        elif command == "freeze":
            freeze_splits(**args)
        else:
            build(**args)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
