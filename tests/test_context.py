"""Context identity, coverage loss and inference/evaluation separation."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from efficient_agentic_inference.context import packet, prepare_context
from efficient_agentic_inference.evaluation import quality
from efficient_agentic_inference.inference import PreparedInference
from efficient_agentic_inference.records import digest, encoded, read_jsonl, verify_artifacts


class ContextContracts(unittest.TestCase):
    def record(self):
        candidates = [
            {"path": f"file{i:02d}.py", "text": ("needle " if i else "unrelated ") + "x" * 1400}
            for i in range(21)
        ]
        return {
            "schema_version": "2.0.0",
            "instance": {
                "instance_id": "fixture",
                "repository": "fixture/repo",
                "base_commit": "a" * 40,
                "issue": "needle",
                "candidates": candidates,
            },
            "preparation_status": "prepared",
            "failure_reason": None,
            "tree_sha256": "b" * 64,
            "candidate_sha256": digest(encoded(candidates)),
        }

    def test_retrieval_is_not_path_prefix_or_gold_selection(self):
        narrowed, metadata = packet(self.record())
        candidates = narrowed["instance"]["candidates"]
        self.assertEqual([c["path"] for c in candidates], [f"file{i:02d}.py" for i in range(1, 21)])
        self.assertTrue(all(len(c["text"]) == 1200 for c in candidates))
        self.assertEqual(narrowed["instance"]["issue"], "needle")
        self.assertEqual(metadata["full_candidate_count"], 21)
        self.assertEqual(metadata["context_candidate_count"], 20)
        PreparedInference.from_record(narrowed)

    def test_source_order_and_external_gold_do_not_change_packet(self):
        record = self.record()
        original, _ = packet(record)
        mutated = copy.deepcopy(record)
        mutated["instance"]["candidates"].reverse()
        mutated["candidate_sha256"] = digest(encoded(mutated["instance"]["candidates"]))
        reordered, _ = packet(mutated)
        self.assertEqual(original, reordered)
        with tempfile.TemporaryDirectory() as temporary:
            gold = Path(temporary) / "gold.json"
            gold.write_text(json.dumps(["file00.py"]))
            first = packet(record)
            gold.write_text(json.dumps(["file01.py"]))
            self.assertEqual(first, packet(record))
            gold.unlink()
            self.assertEqual(first, packet(record))
        forbidden = {**record, "gold_files": ["file00.py"]}
        with self.assertRaises(ValueError):
            packet(forbidden)

    def test_failed_preparation_retained_and_output_immutable(self):
        record = self.record()
        record["instance"]["candidates"] = []
        record.update(
            preparation_status="failed_checkout",
            failure_reason="offline",
            tree_sha256=None,
            candidate_sha256=digest(encoded([])),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs = root / "input.jsonl"
            inputs.write_text(json.dumps(record) + "\n")
            prepare_context(inputs, root / "context", True)
            self.assertEqual(read_jsonl(root / "context/tasks.jsonl"), [record])
            verify_artifacts(root / "context")
            with self.assertRaises(ValueError):
                prepare_context(inputs, root / "context", True)

    def test_context_ceiling_loss_does_not_remove_unreachable_gold(self):
        full = self.record()
        narrowed, _ = packet(full)

        def prediction(record):
            return {
                "disposition": "valid",
                "ranked_files": [],
                "candidate_paths": [c["path"] for c in record["instance"]["candidates"]],
            }

        full_metrics = quality(prediction(full), ["file00.py"], True)
        context_metrics = quality(prediction(narrowed), ["file00.py"], True)
        self.assertEqual(full_metrics["candidate_recall_ceiling"], 1)
        self.assertEqual(context_metrics["candidate_recall_ceiling"], 0)
        self.assertEqual(context_metrics["recall_at_k"]["5"], 0)
        self.assertIsNone(context_metrics["conditional_recall_at_k"]["5"])
