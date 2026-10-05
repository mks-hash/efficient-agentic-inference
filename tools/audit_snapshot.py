"""Rebuild, real-record mutation, base applicability and OS isolation audit."""

import argparse
import json
import platform
import subprocess
from importlib.metadata import version
from pathlib import Path

import pyarrow.parquet as pq
from jsonschema import Draft202012Validator

from efficient_agentic_inference.evaluation import evaluate_saved
from efficient_agentic_inference.records import digest, encoded, jsonl, read_jsonl, verify_artifacts
from efficient_agentic_inference.snapshot import inference_record, projection

ROOT = Path(__file__).resolve().parents[1]


def semantic(path: Path) -> list[dict]:
    return [{k: v for k, v in record.items() if k != "measurements"} for record in read_jsonl(path)]


def audit(snapshot: Path, rebuild: Path, upstream: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    first, second = (
        json.loads((snapshot / "snapshot.json").read_text()),
        json.loads((rebuild / "snapshot.json").read_text()),
    )
    if first != second:
        raise ValueError("Snapshot manifest differs across rebuild")
    comparisons = ["snapshot.json", "inference_inputs/tasks.jsonl", "gold/labels.jsonl"]
    for task in first["population"]:
        for artifact in ("TREE_MANIFEST.json", "CANDIDATE_MANIFEST.json"):
            if task["preparation_status"] == "prepared":
                comparisons.append(f"repos/{task['instance_id']}/{artifact}")
    for name in comparisons:
        if (snapshot / name).read_bytes() != (rebuild / name).read_bytes():
            raise ValueError(f"Rebuild differs: {name}")
    verified_tree_files = 0
    for base in (snapshot, rebuild):
        for task in first["population"]:
            if task["preparation_status"] != "prepared":
                continue
            folder = base / "repos" / task["instance_id"]
            tree_manifest = json.loads((folder / "TREE_MANIFEST.json").read_text())
            expected = {e["path"] for e in tree_manifest["files"] if e["kind"] == "regular"}
            actual = {
                str(p.relative_to(folder / "tree"))
                for p in (folder / "tree").rglob("*")
                if p.is_file() or p.is_symlink()
            }
            if actual != expected:
                raise ValueError("Exported tree contains missing/unexpected files or symlinks")
            for entry in tree_manifest["files"]:
                if entry["kind"] == "regular":
                    path = folder / "tree" / entry["path"]
                    if path.is_symlink() or digest(path.read_bytes()) != entry["content_sha256"]:
                        raise ValueError("Exported tree content mismatch")
                    verified_tree_files += 1
    inputs = read_jsonl(snapshot / "inference_inputs/tasks.jsonl")
    raw_rows = {r["instance_id"]: r for r in pq.read_table(upstream / "dev.parquet").to_pylist()}
    mutated_inputs, applicability = [], []
    for original in inputs:
        iid = original["instance"]["instance_id"]
        raw = raw_rows[iid]
        if original["preparation_status"] != "prepared":
            mutated_inputs.append(original)
            applicability.append({"instance_id": iid, "status": "NOT_RUN"})
            continue
        folder = snapshot / "repos" / iid
        tree_manifest = json.loads((folder / "TREE_MANIFEST.json").read_text())
        candidate_manifest = json.loads((folder / "CANDIDATE_MANIFEST.json").read_text())
        mutant = dict(raw)
        for key in set(raw) - set(projection(raw)):
            mutant[key] = "FORBIDDEN_FIELD_MUTATION"
        mutant["future_upstream_field"] = "FORBIDDEN_FIELD_MUTATION"
        record, candidates = inference_record(projection(mutant), folder / "tree", tree_manifest)
        if record != original or candidates != candidate_manifest:
            raise ValueError("Forbidden-field mutation changed inference/candidates/order")
        mutated_inputs.append(record)
        check = subprocess.run(
            ["git", "apply", "--check", "--"],
            input=raw["patch"].encode(),
            cwd=folder / "tree",
            capture_output=True,
            check=False,
        )
        applicability.append(
            {
                "instance_id": iid,
                "status": "PASS" if not check.returncode else "FAIL",
                "reason": check.stderr.decode().strip() or None,
            }
        )
    if any(item["status"] != "PASS" for item in applicability):
        raise ValueError(
            "Base applicability audit incomplete/failed; preparation remains in snapshot"
        )
    mutant_path = output / "mutated-inputs.jsonl"
    mutant_path.write_bytes(jsonl(mutated_inputs))
    if mutant_path.read_bytes() != (snapshot / "inference_inputs/tasks.jsonl").read_bytes():
        raise ValueError("Mutated inference bytes differ")
    for name, inputs_path in (
        ("predict-original", snapshot / "inference_inputs/tasks.jsonl"),
        ("predict-mutated", mutant_path),
    ):
        subprocess.run(
            [str(ROOT / "tools/predict-isolated.sh"), str(inputs_path), str(output / name)],
            check=True,
        )
        verify_artifacts(output / name)
    original_predictions = output / "predict-original/predictions.jsonl"
    mutant_predictions = output / "predict-mutated/predictions.jsonl"
    if semantic(original_predictions) != semantic(mutant_predictions):
        raise ValueError("Forbidden-field mutation changed predictions")
    actual = evaluate_saved(
        output / "predict-original", snapshot / "gold/labels.jsonl", output / "evaluate-original"
    )
    # Gold mutation occurs between two physically isolated prediction processes.
    mutant_gold = read_jsonl(snapshot / "gold/labels.jsonl")
    for record in mutant_gold:
        record.update(
            label_status="labeled",
            failure_reason=None,
            changes=[
                {
                    "path": "__audit_missing__.py",
                    "old_path": None,
                    "new_path": "__audit_missing__.py",
                    "status": "added",
                    "category": "implementation",
                    "binary": False,
                }
            ],
        )
    gold_path = output / "mutated-labels.jsonl"
    gold_path.write_bytes(jsonl(mutant_gold))
    subprocess.run(
        [
            str(ROOT / "tools/predict-isolated.sh"),
            str(snapshot / "inference_inputs/tasks.jsonl"),
            str(output / "predict-gold-mutated"),
        ],
        check=True,
    )
    if semantic(original_predictions) != semantic(
        output / "predict-gold-mutated/predictions.jsonl"
    ):
        raise ValueError("Gold mutation changed predictions")
    changed = evaluate_saved(
        output / "predict-gold-mutated", gold_path, output / "evaluate-mutated"
    )
    if actual["all_files"] == changed["all_files"]:
        raise ValueError("Gold mutation did not change evaluation; audit inconclusive")
    repeated = evaluate_saved(
        output / "predict-original", snapshot / "gold/labels.jsonl", output / "evaluate-repeated"
    )
    if actual != repeated:
        raise ValueError("Repeated evaluation differs")
    # Independently published schemas validate every artifact record.
    for name, records in (
        ("inference", inputs),
        ("prediction", read_jsonl(original_predictions)),
        ("evaluation", read_jsonl(snapshot / "gold/labels.jsonl")),
    ):
        validator = Draft202012Validator(
            json.loads((ROOT / f"schemas/v2/{name}.schema.json").read_text())
        )
        validator.check_schema(validator.schema)
        for record in records:
            validator.validate(record)
    dev = json.loads((ROOT / "splits/dev-v1.json").read_text())
    final = json.loads((ROOT / "splits/evaluation-v1.json").read_text())
    overlap = set(r["instance_id"] for r in dev["instances"]) & set(final["instance_ids"])
    if overlap:
        raise ValueError("Dev/final ID overlap")
    report = {
        "schema_version": "1.0.0",
        "status": "PASS",
        "selected": first["selected"],
        "code_commit": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
        .decode()
        .strip(),
        "code_dirty": bool(
            subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain"]).strip()
        ),
        "environment": {
            "builder_python": platform.python_version(),
            "pyarrow": version("pyarrow"),
            "git": subprocess.check_output(["git", "--version"]).decode().strip(),
            "predict_python": json.loads((output / "predict-original/manifest.json").read_text())[
                "python"
            ],
        },
        "hardware_cpu": next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            platform.machine(),
        ),
        "snapshot_sha256": digest((snapshot / "snapshot.json").read_bytes()),
        "inputs_sha256": first["inputs_sha256"],
        "gold_sha256": first["gold_sha256"],
        "semantic_predictions_sha256": digest(encoded(semantic(original_predictions))),
        "rebuild_compared_artifacts": len(comparisons),
        "rebuild_identical": True,
        "verified_regular_tree_files_across_both_builds": verified_tree_files,
        "forbidden_fields_inputs_candidates_order_predictions_identical": True,
        "gold_mutation_predictions_identical": True,
        "gold_mutation_metrics_changed": True,
        "repeated_evaluation_identical": True,
        "schemas_valid": True,
        "dev_final_id_overlap": [],
        "base_patch_applicability": applicability,
        "isolation": json.loads((output / "predict-original/isolation.json").read_text()),
        "limits": [
            "Same-host fresh-directory rebuild, not an independently operated second machine",
            "Exact ID/normalized issue overlap audit; no near-duplicate/pretraining guarantee",
            "Small development pilot; no final Verified inference or labels generated",
        ],
    }
    (output / "audit.json").write_bytes(encoded(report))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--rebuild", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(
                args.snapshot.resolve(),
                args.rebuild.resolve(),
                args.upstream.resolve(),
                args.output.resolve(),
            ),
            indent=2,
        )
    )
