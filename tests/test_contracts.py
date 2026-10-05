"""Independent gold expectations, leakage checks and failure accounting."""

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import ValidationError

from efficient_agentic_inference.cli import digest, run, validate
from efficient_agentic_inference.localization import (
    Task,
    evaluate,
    prediction_error,
    rank_files,
    summarize,
)

ROOT = Path(__file__).resolve().parents[1]


def task_record():
    return {
        "instance_id": "unit",
        "repository": "synthetic/unit",
        "base_commit": "fixture-v1",
        "issue": "cache expiry",
        "candidates": [
            {"path": "z.py", "text": "cache expiry"},
            {"path": "a.py", "text": "parser number"},
        ],
    }


class LocalizationContracts(unittest.TestCase):
    def test_gold_never_accepted_as_task_input(self):
        record = task_record()
        record["patch"] = "a solution"
        with self.assertRaises(ValueError):
            Task.from_record(record)

    def test_invalid_candidate_paths_rejected(self):
        for path in ("/tmp/file", "../file", "a/../file", "a//file", "a\\file", "./file"):
            record = task_record()
            record["candidates"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                Task.from_record(record)

    def test_duplicate_candidates_rejected(self):
        record = task_record()
        record["candidates"].append(record["candidates"][0])
        with self.assertRaises(ValueError):
            Task.from_record(record)

    def test_rank_order_and_stable_tie(self):
        self.assertEqual(rank_files(Task.from_record(task_record())), ["z.py", "a.py"])
        record = task_record()
        record["issue"] = "unmatched"
        self.assertEqual(rank_files(Task.from_record(record)), ["a.py", "z.py"])

    def test_independently_calculated_metrics(self):
        metrics = evaluate(["miss.py", "b.py", "a.py"], ["a.py", "b.py", "new.py"])
        self.assertEqual(metrics["recall_at_k"]["1"], 0)
        self.assertAlmostEqual(metrics["recall_at_k"]["3"], 2 / 3)
        self.assertEqual(metrics["precision_at_k"]["5"], 2 / 5)
        self.assertEqual(metrics["mrr"], 1 / 2)
        self.assertFalse(metrics["strict_success_at_k"]["10"])

    def test_missing_prediction_slots_are_precision_misses(self):
        metrics = evaluate(["a.py"], ["a.py"])
        self.assertEqual(metrics["precision_at_k"]["5"], 1 / 5)
        self.assertTrue(metrics["strict_success_at_k"]["5"])

    def test_invalid_output_is_not_repaired(self):
        self.assertIsNotNone(prediction_error(["a.py", "a.py"], {"a.py"}))
        self.assertIsNotNone(prediction_error(["unknown.py"], {"a.py"}))
        self.assertIsNotNone(prediction_error("a.py", {"a.py"}))
        metrics = evaluate(["a.py"], ["a.py"], "invalid_output")
        self.assertEqual(metrics["recall_at_k"]["5"], 0)
        self.assertFalse(metrics["strict_success_at_k"]["5"])

    def test_empty_gold_is_not_success(self):
        metrics = evaluate([], [])
        self.assertIsNone(metrics["recall_at_k"]["5"])
        self.assertIsNone(metrics["mrr"])
        self.assertFalse(metrics["strict_success_at_k"]["5"])

    def test_failure_costs_stay_in_numerator(self):
        records = [
            {
                "metrics": evaluate(["a.py"], ["a.py"]),
                "disposition": "valid",
                "measurements": {"wall_ms": 2, "monetary_usd": 1},
            },
            {
                "metrics": evaluate([], ["a.py"], "timeout"),
                "disposition": "timeout",
                "measurements": {"wall_ms": 10, "monetary_usd": 2},
            },
        ]
        summary = summarize(records)
        self.assertEqual(summary["cost_per_success_usd"], 3)
        self.assertEqual(summary["strict_success_rate"], 0.5)
        records[1]["measurements"]["monetary_usd"] = None
        self.assertIsNone(summarize(records)["cost_per_success_usd"])

    def test_zero_success_has_undefined_cps(self):
        summary = summarize(
            [
                {
                    "metrics": evaluate([], ["a.py"]),
                    "disposition": "valid",
                    "measurements": {"wall_ms": 1, "monetary_usd": 0},
                }
            ]
        )
        self.assertIsNone(summary["cost_per_success_usd"])
        self.assertEqual(summary["cost_per_success_reason"], "zero_successes")


class RunnerContracts(unittest.TestCase):
    def args(self, output):
        return argparse.Namespace(
            project_root=ROOT,
            tasks=ROOT / "examples/localization-v1/tasks.jsonl",
            gold=ROOT / "examples/localization-v1/gold.jsonl",
            output=output,
            limit=10,
            synthetic=True,
        )

    def test_synthetic_end_to_end_schema_hashes_and_immutable_output(self):
        with tempfile.TemporaryDirectory() as folder:
            args = self.args(Path(folder) / "fixture")
            summary = run(args)
            self.assertEqual(summary["attempted_tasks"], 3)
            self.assertEqual(summary["strict_successes"], 2)
            self.assertAlmostEqual(summary["mean_recall_at_k"]["5"], 2 / 3)
            self.assertIsNone(summary["cost_per_success_usd"])
            manifest = json.loads((args.output / "manifest.json").read_text())
            validate(manifest, ROOT / "schemas/v1/experiment.schema.json")
            self.assertTrue(manifest["synthetic"])
            self.assertEqual(manifest["evidence"]["economics"]["status"], "UNKNOWN")
            for name, sha in json.loads((args.output / "checksums.json").read_text()).items():
                self.assertEqual(digest((args.output / name).read_bytes()), sha)
            with self.assertRaises(ValueError):
                run(args)
            manifest["model"] = {"repo": "unversioned"}
            with self.assertRaises(ValidationError):
                validate(manifest, ROOT / "schemas/v1/experiment.schema.json")

    def test_runtime_failures_still_produce_all_records(self):
        with tempfile.TemporaryDirectory() as folder:
            args = self.args(Path(folder) / "failed")
            with patch(
                "efficient_agentic_inference.cli.rank_files", side_effect=RuntimeError("oops")
            ):
                summary = run(args)
            self.assertEqual(summary["attempted_tasks"], 3)
            self.assertEqual(summary["failed_outputs"], 3)
            self.assertEqual(summary["strict_successes"], 0)
            self.assertEqual(summary["mean_recall_at_k"]["5"], 0)

    def test_invalid_raw_output_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            args = self.args(Path(folder) / "invalid")
            with patch("efficient_agentic_inference.cli.rank_files", return_value=["unknown.py"]):
                summary = run(args)
            self.assertEqual(summary["failed_outputs"], 3)
            first = json.loads((args.output / "predictions.jsonl").read_text().splitlines()[0])
            self.assertEqual(first["raw_output"], '["unknown.py"]')
            self.assertEqual(first["ranked_files"], [])
            self.assertEqual(first["disposition"], "invalid_output")

    def test_gold_join_mismatch_aborts_before_writing_run(self):
        with tempfile.TemporaryDirectory() as folder:
            args = self.args(Path(folder) / "mismatch")
            gold = Path(folder) / "gold.jsonl"
            gold.write_text('{"instance_id":"other","changed_files":["a.py"]}\n')
            args.gold = gold
            with self.assertRaises(ValueError):
                run(args)
            self.assertFalse(args.output.exists())


if __name__ == "__main__":
    unittest.main()
