"""Independent label fixtures, transformation independence and immutable programs."""

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

from efficient_agentic_inference.evaluation import evaluate_saved
from efficient_agentic_inference.inference import PreparedInference
from efficient_agentic_inference.labeler import EvaluationInstance, labels
from efficient_agentic_inference.predict import predict
from efficient_agentic_inference.records import digest, encoded, jsonl, read_jsonl, write_artifacts
from efficient_agentic_inference.snapshot import export_base, inference_record, projection, select

MODIFIED = """diff --git a/a.py b/a.py
index 7898192..6178079 100644
--- a/a.py
+++ b/a.py
@@ -1 +1 @@
-a
+b
"""
ADDED = """diff --git a/new.py b/new.py
new file mode 100644
index 0000000..7898192
--- /dev/null
+++ b/new.py
@@ -0,0 +1 @@
+a
"""
DELETED = """diff --git a/old.py b/old.py
deleted file mode 100644
index 7898192..0000000
--- a/old.py
+++ /dev/null
@@ -1 +0,0 @@
-a
"""
RENAMED = """diff --git a/old.py b/new.py
similarity index 100%
rename from old.py
rename to new.py
"""


def allowed(instance_id="unit"):
    return {
        "instance_id": instance_id,
        "repo": "synthetic/example",
        "base_commit": "a" * 40,
        "problem_statement": "cache expiry",
    }


def envelope(instance_id="unit"):
    candidates = [
        {"path": "a.py", "text": "cache expiry"},
        {"path": "b.py", "text": "parser number"},
    ]
    r = allowed(instance_id)
    return {
        "schema_version": "2.0.0",
        "instance": {
            "instance_id": r["instance_id"],
            "repository": r["repo"],
            "base_commit": r["base_commit"],
            "issue": r["problem_statement"],
            "candidates": candidates,
        },
        "preparation_status": "prepared",
        "failure_reason": None,
        "tree_sha256": "a" * 64,
        "candidate_sha256": digest(encoded(candidates)),
    }


def semantic_predictions(path):
    return [
        {k: v for k, v in r.items() if k != "measurements"}
        for r in (json.loads(line) for line in path.read_text().splitlines())
    ]


class LabelerContracts(unittest.TestCase):
    def test_modify_add_delete_rename_against_manual_gold(self):
        for patch_text, path, status, old, new in [
            (MODIFIED, "a.py", "modified", "a.py", "a.py"),
            (ADDED, "new.py", "added", None, "new.py"),
            (DELETED, "old.py", "deleted", "old.py", None),
            (RENAMED, "old.py", "renamed", "old.py", "new.py"),
        ]:
            with self.subTest(status=status):
                record = labels("fixture", patch_text)
                self.assertEqual(record.label_status, "labeled")
                self.assertEqual(
                    record.changes[0],
                    {
                        "path": path,
                        "status": status,
                        "old_path": old,
                        "new_path": new,
                        "category": "implementation",
                        "binary": False,
                    },
                )

    def test_multifile_and_tests_are_retained(self):
        test_patch = MODIFIED.replace("a.py", "tests/test_a.py")
        record = labels("fixture", ADDED + test_patch)
        self.assertEqual([r["path"] for r in record.changes], ["new.py", "tests/test_a.py"])
        self.assertEqual(record.changes[1]["category"], "test")

    def test_quoted_unicode_and_space_paths(self):
        patch_text = RENAMED.replace("rename from old.py", 'rename from "old \\303\\251.py"')
        record = labels("fixture", patch_text)
        self.assertEqual(record.changes[0]["path"], "old é.py")
        patch_text = MODIFIED.replace("a.py", "space name.py")
        self.assertEqual(labels("fixture", patch_text).changes[0]["path"], "space name.py")

    def test_mode_only_diff_has_explicit_status(self):
        record = labels("fixture", "diff --git a/a.py b/a.py\nold mode 100644\nnew mode 100755\n")
        self.assertEqual(record.changes[0]["status"], "mode_changed")

    def test_binary_diff_is_retained(self):
        record = labels(
            "fixture",
            "diff --git a/image.png b/image.png\nindex 1234567..7654321 100644\n"
            "Binary files a/image.png and b/image.png differ\n",
        )
        self.assertEqual(record.label_status, "labeled")
        self.assertTrue(record.changes[0]["binary"])
        self.assertEqual(record.changes[0]["category"], "non_code")

    def test_empty_invalid_and_unsafe_patches_are_explicit(self):
        self.assertEqual(labels("fixture", "").label_status, "empty_patch")
        self.assertNotEqual(labels("fixture", "invalid diff").label_status, "labeled")
        self.assertNotEqual(
            labels("fixture", MODIFIED.replace("a.py", "../escape.py")).label_status, "labeled"
        )


class PipelineContracts(unittest.TestCase):
    def test_published_schemas_validate_fixture_inputs_predictions_and_labels(self):
        project = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs = project / "examples/localization-v2/tasks.jsonl"
            predict(inputs, root / "predictions", synthetic=True)
            for name, path in (
                ("inference", inputs),
                ("prediction", root / "predictions/predictions.jsonl"),
                ("evaluation", project / "examples/localization-v2/gold.jsonl"),
            ):
                schema = json.loads((project / f"schemas/v2/{name}.schema.json").read_text())
                Draft202012Validator.check_schema(schema)
                for record in read_jsonl(path):
                    Draft202012Validator(schema).validate(record)

    def test_saved_evaluation_includes_failure_costs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs, gold = root / "inputs.jsonl", root / "labels.jsonl"
            inputs.write_bytes(jsonl([envelope("a"), envelope("b")]))
            predict(inputs, root / "original", synthetic=True)
            records = read_jsonl(root / "original/predictions.jsonl")
            records[0]["measurements"]["monetary_usd"] = 2
            records[1]["measurements"]["monetary_usd"] = 4
            records[1].update(
                disposition="runtime_error", failure_reason="fixture failure", ranked_files=[]
            )
            payload = jsonl(records)
            write_artifacts(
                root / "priced-fixture",
                {
                    "predictions.jsonl": payload,
                    "predictions.sha256": (digest(payload) + "\n").encode(),
                    "manifest.json": (root / "original/manifest.json").read_bytes(),
                },
            )
            gold.write_bytes(
                jsonl([labels("a", MODIFIED).to_record(), labels("b", MODIFIED).to_record()])
            )
            summary = evaluate_saved(root / "priced-fixture", gold, root / "evaluated")
            self.assertEqual(summary["total_monetary_usd"], 6)
            self.assertEqual(summary["cost_per_success_usd"], 6)

    def test_predict_without_any_evaluation_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs = root / "inputs.jsonl"
            inputs.write_bytes(jsonl([envelope()]))
            output = root / "predictions"
            self.assertEqual(predict(inputs, output)["attempted"], 1)
            self.assertEqual(
                semantic_predictions(output / "predictions.jsonl")[0]["ranked_files"],
                ["a.py", "b.py"],
            )
            with self.assertRaises(ValueError):
                predict(inputs, output)

    def test_gold_mutation_changes_only_metrics(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs, gold = root / "inputs.jsonl", root / "labels.jsonl"
            inputs.write_bytes(jsonl([envelope()]))
            predict(inputs, root / "p1")
            gold.write_bytes(jsonl([labels("unit", MODIFIED).to_record()]))
            original = evaluate_saved(root / "p1", gold, root / "e1")
            gold.write_bytes(jsonl([labels("unit", ADDED).to_record()]))
            predict(inputs, root / "p2")
            mutated = evaluate_saved(root / "p2", gold, root / "e2")
            self.assertEqual(
                semantic_predictions(root / "p1/predictions.jsonl"),
                semantic_predictions(root / "p2/predictions.jsonl"),
            )
            self.assertEqual(original["all_files"]["mean_recall_at_k"]["5"], 1)
            self.assertEqual(mutated["all_files"]["mean_recall_at_k"]["5"], 0)
            self.assertIsNone(mutated["all_files"]["conditional_recall_at_k"]["5"])

    def test_forbidden_source_fields_do_not_change_inputs_candidates_or_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            (tree / "a.py").write_text("cache expiry")
            manifest = {
                "files": [
                    {
                        "path": "a.py",
                        "kind": "regular",
                        "size": 12,
                        "content_sha256": digest(b"cache expiry"),
                    }
                ]
            }
            raw = {
                **allowed(),
                "patch": MODIFIED,
                "test_patch": ADDED,
                "hints_text": "hint",
                "FAIL_TO_PASS": ["future test"],
                "difficulty": "easy",
            }
            original = inference_record(projection(raw), tree, manifest)
            mutated = {
                **raw,
                **{k: "mutated" for k in raw if k not in allowed()},
                "future_upstream_field": "solution",
            }
            self.assertEqual(original, inference_record(projection(mutated), tree, manifest))
            with self.assertRaises(ValueError):
                inference_record(raw, tree, manifest)

    def test_prediction_failures_and_unknown_labels_do_not_disappear(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs, gold = root / "inputs.jsonl", root / "labels.jsonl"
            inputs.write_bytes(jsonl([envelope()]))
            with patch(
                "efficient_agentic_inference.predict.rank_files", side_effect=RuntimeError("boom")
            ):
                predict(inputs, root / "predictions")
            gold.write_bytes(jsonl([labels("unit", MODIFIED).to_record()]))
            summary = evaluate_saved(root / "predictions", gold, root / "evaluated")
            self.assertEqual(summary["selected"], 1)
            self.assertEqual(summary["failed_prediction"], 1)
            self.assertEqual(summary["all_files"]["strict_success_rate_at_5"], 0)
            gold.write_bytes(
                jsonl([EvaluationInstance("unit", "parse_failure", "bad", ()).to_record()])
            )
            summary = evaluate_saved(root / "predictions", gold, root / "unknown")
            self.assertIsNone(summary["all_files"]["mean_recall_at_k"]["5"])
            self.assertEqual(summary["all_files"]["unknown_label_tasks"], 1)

    def test_failed_preparation_remains_in_denominator(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record = envelope()
            record.update(
                preparation_status="failed_checkout",
                failure_reason="missing commit",
                tree_sha256=None,
                candidate_sha256=digest(encoded([])),
            )
            record["instance"]["candidates"] = []
            inputs, gold = root / "inputs.jsonl", root / "labels.jsonl"
            inputs.write_bytes(jsonl([record]))
            gold.write_bytes(jsonl([labels("unit", MODIFIED).to_record()]))
            predict(inputs, root / "predictions")
            summary = evaluate_saved(root / "predictions", gold, root / "evaluated")
            self.assertEqual(summary["selected"], 1)
            self.assertEqual(summary["failed_preparation"], 1)
            self.assertEqual(summary["all_files"]["mean_recall_at_k"]["5"], 0)

    def test_checksums_and_gold_join_are_enforced(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs, gold = root / "inputs.jsonl", root / "labels.jsonl"
            inputs.write_bytes(jsonl([envelope()]))
            predict(inputs, root / "predictions")
            gold.write_bytes(jsonl([labels("other", MODIFIED).to_record()]))
            with self.assertRaises(ValueError):
                evaluate_saved(root / "predictions", gold, root / "evaluated")
            path = root / "predictions/predictions.jsonl"
            path.write_text("tampered")
            with self.assertRaises(ValueError):
                evaluate_saved(root / "predictions", gold, root / "tampered")

    def test_candidate_checksum_and_extra_fields_rejected(self):
        record = envelope()
        record["instance"]["candidates"].reverse()
        with self.assertRaises(ValueError):
            PreparedInference.from_record(record)
        record = envelope()
        record["patch"] = MODIFIED
        with self.assertRaises(ValueError):
            PreparedInference.from_record(record)

    def test_split_selection_ignores_gold_and_excludes_final_overlap(self):
        dev = [
            {**allowed(str(i)), "patch": MODIFIED, "problem_statement": f"issue {i}"}
            for i in range(5)
        ]
        final = [dev[0]]
        selected, exclusions = select(dev, final, 3, "seed")
        self.assertNotIn("0", [r["instance_id"] for r in selected])
        self.assertEqual(exclusions[0]["instance_id"], "0")
        mutant = copy.deepcopy(dev)
        for record in mutant:
            record["patch"] = ADDED
        self.assertEqual(select(dev, final, 3, "seed"), select(mutant, final, 3, "seed"))

    def test_exact_git_tree_export_ignores_archive_attributes_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "source"
            repo.mkdir()
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            (repo / "a.py").write_text("cache expiry")
            (repo / ".gitattributes").write_text("a.py export-ignore\n")
            (repo / "link.py").symlink_to("/outside/secret")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-m",
                    "base",
                ],
                check=True,
                capture_output=True,
            )
            commit = (
                subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"])
                .decode()
                .strip()
            )
            cache = root / "cache"
            cache.mkdir()
            subprocess.run(
                ["git", "clone", "--bare", str(repo), str(cache / "synthetic__example")],
                check=True,
                capture_output=True,
            )
            first = export_base("synthetic/example", commit, cache, root / "tree1", True)
            second = export_base("synthetic/example", commit, cache, root / "tree2", True)
            self.assertEqual(first, second)
            self.assertTrue((root / "tree1/a.py").is_file())
            self.assertFalse((root / "tree1/link.py").exists())
            self.assertFalse((root / "tree1/.git").exists())
            row = {**allowed(), "base_commit": commit}
            self.assertEqual(
                inference_record(row, root / "tree1", first),
                inference_record(row, root / "tree2", second),
            )
