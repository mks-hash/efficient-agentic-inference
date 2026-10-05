"""Independent quality and input contract expectations."""

import unittest

from efficient_agentic_inference.localization import (
    Task,
    evaluate,
    prediction_error,
    rank_files,
    summarize,
)


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


if __name__ == "__main__":
    unittest.main()
