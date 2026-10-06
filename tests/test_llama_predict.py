"""Independently specified API evidence invariants; no model quality claims."""

import copy
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from efficient_agentic_inference.inference import PreparedInference
from efficient_agentic_inference.llama_predict import classify, consume_event, infer, token_ids
from efficient_agentic_inference.records import digest, encoded

CONFIG = {"decoding": {"max_output_tokens": 512}, "execution": {"context_tokens": 16384}}


def evidence():
    return {
        "input_token_ids": [101, 102],
        "output_token_ids": [201, 202],
        "raw_output": '["src/a.py"]',
        "final_response": {
            "truncated": False,
            "stop_type": "eos",
            "tokens_evaluated": 2,
            "tokens_predicted": 2,
            "generation_settings": {"seed": 0, "temperature": 0, "n_predict": 512},
        },
    }


class ModelEvidenceContracts(unittest.TestCase):
    def test_strict_output_and_token_provenance(self):
        self.assertEqual(classify(evidence(), {"src/a.py"}, CONFIG), ["src/a.py"])
        for raw in (
            '```json\n["src/a.py"]\n```',
            '["src/a.py", "src/a.py"]',
            '["secret.py"]',
            '{"files": ["src/a.py"]}',
        ):
            record = evidence()
            record["raw_output"] = raw
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                classify(record, {"src/a.py"}, CONFIG)
        for field, value in (
            ("truncated", True),
            ("stop_type", "limit"),
            ("tokens_evaluated", 3),
            ("tokens_predicted", 3),
        ):
            record = evidence()
            record["final_response"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                classify(record, {"src/a.py"}, CONFIG)
        record = evidence()
        record["final_response"]["generation_settings"]["temperature"] = 0.7
        with self.assertRaisesRegex(ValueError, "decoding_mismatch"):
            classify(record, {"src/a.py"}, CONFIG)

    def test_progress_not_counted_as_generated_token(self):
        record = {"output_token_ids": [], "raw_output": "", "final_response": None}
        consume_event({"prompt_progress": {"processed": 2}, "tokens": [-1]}, record)
        consume_event({"tokens": [7], "content": "["}, record)
        consume_event({"stop": True, "tokens": [], "content": ""}, record)
        self.assertEqual(record["output_token_ids"], [7])
        self.assertEqual(record["raw_output"], "[")
        self.assertFalse(token_ids([True]))
        self.assertFalse(token_ids([-1]))

    def task(self):
        candidates = [{"path": "src/a.py", "text": "def broken(): pass"}]
        return PreparedInference.from_record(
            {
                "schema_version": "2.0.0",
                "instance": {
                    "instance_id": "synthetic",
                    "repository": "fixture/repo",
                    "base_commit": "a" * 40,
                    "issue": "Fix broken",
                    "candidates": candidates,
                },
                "preparation_status": "prepared",
                "failure_reason": None,
                "tree_sha256": "b" * 64,
                "candidate_sha256": digest(encoded(candidates)),
            }
        )

    def test_timeout_retains_partial_output_without_retry(self):
        def interrupted(payload, deadline, record, trace):
            consume_event({"tokens": [7, 8], "content": '["src/'}, record)
            raise TimeoutError("expired")

        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    side_effect=[
                        {"prompt": "native"},
                        {"tokens": [101, 102]},
                    ],
                ),
                patch(
                    "efficient_agentic_inference.llama_predict.stream", side_effect=interrupted
                ) as generate,
            ):
                record = infer(self.task(), CONFIG, "system", folder, time.monotonic() + 10)
            self.assertEqual(generate.call_count, 1)
            self.assertEqual(record["disposition"], "runtime_error")
            self.assertEqual(record["ranked_files"], [])
            self.assertEqual(record["raw_output"], '["src/')
            self.assertEqual(record["measurements"]["output_tokens"], 2)
            self.assertIsNone(record["measurements"]["cpu_ms"])
            self.assertIsNone(record["measurements"]["monetary_usd"])
            saved = json.loads((folder / "evidence.json").read_text())
            self.assertEqual(saved["output_token_ids"], [7, 8])

    def test_overflow_never_generates_or_truncates_input(self):
        config = copy.deepcopy(CONFIG)
        config["execution"]["context_tokens"] = 513
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    side_effect=[
                        {"prompt": "native"},
                        {"tokens": [101, 102]},
                    ],
                ),
                patch("efficient_agentic_inference.llama_predict.stream") as generate,
            ):
                record = infer(
                    self.task(), config, "system", Path(temporary), time.monotonic() + 10
                )
            generate.assert_not_called()
            self.assertIn("context_overflow", record["failure_reason"])
            self.assertEqual(record["measurements"]["input_tokens"], 2)
