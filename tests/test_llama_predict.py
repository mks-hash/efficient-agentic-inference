"""Independently specified API evidence invariants; no model quality claims."""

import copy
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

from efficient_agentic_inference.inference import PreparedInference
from efficient_agentic_inference.llama_predict import (
    candidate_output_schema,
    classify,
    consume_event,
    gpu_layers,
    gpu_seconds,
    infer,
    output_constraint,
    require_full_offload,
    token_ids,
)
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
    def test_candidate_schema_uses_only_paths_and_does_not_claim_uniqueness(self):
        paths = ['src/quo"te.py', "src/é.py", "src/a.py"]
        schema = candidate_output_schema(paths)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for allowed in ([], [paths[0]], [paths[1], paths[2]], [paths[2]] * 10):
            self.assertTrue(validator.is_valid(allowed))
        for forbidden in (["hidden.py"], paths * 4, {"paths": paths}, [3]):
            self.assertFalse(validator.is_valid(forbidden))
        self.assertEqual(schema["items"]["enum"], sorted(paths))
        self.assertNotIn("uniqueItems", schema)
        empty = Draft202012Validator(candidate_output_schema([]))
        self.assertTrue(empty.is_valid([]))
        self.assertFalse(empty.is_valid(["src/a.py"]))
        for invalid in (["../escape.py"], ["src/a.py", "src/a.py"]):
            with self.assertRaises(ValueError):
                candidate_output_schema(invalid)
        self.assertIsNone(output_constraint(CONFIG))
        for unsupported in (
            {},
            {"policy": "arbitrary"},
            {"policy": "candidate-json-array-v1", "uniqueItems": True},
        ):
            with self.assertRaises(ValueError):
                output_constraint({"output_constraint": unsupported})

    def test_effective_grammar_is_required_but_duplicates_still_fail(self):
        config = {**CONFIG, "output_constraint": {"policy": "candidate-json-array-v1"}}
        record = evidence()
        with self.assertRaisesRegex(ValueError, "grammar_missing"):
            classify(record, {"src/a.py"}, config)
        record["final_response"]["generation_settings"].update(
            grammar='root ::= "[]"', grammar_lazy=False
        )
        self.assertEqual(classify(record, {"src/a.py"}, config), ["src/a.py"])
        with self.assertRaisesRegex(ValueError, "unexpected_constraint"):
            classify(record, {"src/a.py"}, CONFIG)
        record["raw_output"] = '["src/a.py", "src/a.py"]'
        with self.assertRaisesRegex(ValueError, "duplicate"):
            classify(record, {"src/a.py"}, config)
        record["final_response"]["generation_settings"]["grammar_lazy"] = True
        with self.assertRaisesRegex(ValueError, "not_eager"):
            classify(record, {"src/a.py"}, config)

    def test_constraint_changes_only_completion_request_not_evidence_prompt(self):
        calls = []
        for constrained in (False, True):
            config = copy.deepcopy(CONFIG)
            if constrained:
                config["output_constraint"] = {"policy": "candidate-json-array-v1"}
            with tempfile.TemporaryDirectory() as temporary:
                with (
                    patch(
                        "efficient_agentic_inference.llama_predict.post",
                        side_effect=[{"prompt": "native"}, {"tokens": [101, 102]}],
                    ) as api,
                    patch("efficient_agentic_inference.llama_predict.stream") as generate,
                ):
                    infer(self.task(), config, "system", Path(temporary), time.monotonic() + 10)
                saved = json.loads((Path(temporary) / "evidence.json").read_text())
                calls.append((api.call_args_list, generate.call_args.args[0], saved))
        self.assertEqual(
            [call.args[:2] for call in calls[0][0]], [call.args[:2] for call in calls[1][0]]
        )
        free_payload, constrained_payload = calls[0][1], calls[1][1]
        schema = constrained_payload.pop("json_schema")
        self.assertEqual(free_payload, constrained_payload)
        self.assertEqual(schema["items"]["enum"], ["src/a.py"])
        self.assertEqual(calls[1][2]["output_schema_sha256"], digest(encoded(schema)))
        self.assertEqual(calls[0][2]["input_token_ids"], calls[1][2]["input_token_ids"])

    def test_gpu_flags_do_not_invent_utilization_or_allow_cpu_fallback(self):
        self.assertEqual(gpu_layers(CONFIG), "0")
        self.assertEqual(gpu_seconds(CONFIG), 0)
        cuda = {"execution": {"device": "cuda"}}
        self.assertEqual(gpu_layers(cuda), "999")
        self.assertIsNone(gpu_seconds(cuda))
        require_full_offload("load_tensors: offloaded 37/37 layers to GPU")
        for log in (
            "CPU model loaded",
            "offloaded 0/37 layers to GPU",
            "offloaded 20/37 layers to GPU",
        ):
            with self.subTest(log=log), self.assertRaises(ValueError):
                require_full_offload(log)
        with self.assertRaises(ValueError):
            gpu_layers({"execution": {"device": "unknown"}})

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

    def test_nonthinking_request_is_explicit_and_native_suffix_checked(self):
        config = copy.deepcopy(CONFIG)
        suffix = "<|im_start|>assistant\n<think>\n\n</think>\n\n"
        config["native_template"] = {"enable_thinking": False, "expected_rendered_suffix": suffix}
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    side_effect=[{"prompt": "native\n" + suffix}, {"tokens": [101, 102]}],
                ) as api,
                patch("efficient_agentic_inference.llama_predict.stream") as generate,
            ):
                infer(self.task(), config, "system", Path(temporary), time.monotonic() + 10)
            self.assertEqual(
                api.call_args_list[0].args[1]["chat_template_kwargs"], {"enable_thinking": False}
            )
            self.assertEqual(generate.call_count, 1)
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    return_value={"prompt": "native<think>"},
                ),
                patch("efficient_agentic_inference.llama_predict.stream") as generate,
            ):
                record = infer(
                    self.task(), config, "system", Path(temporary), time.monotonic() + 10
                )
            generate.assert_not_called()
            self.assertIn("nonthinking_native_suffix_mismatch", record["failure_reason"])

    def test_historical_template_request_stays_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    side_effect=[{"prompt": "native"}, {"tokens": [101, 102]}],
                ) as api,
                patch("efficient_agentic_inference.llama_predict.stream"),
            ):
                infer(self.task(), CONFIG, "system", Path(temporary), time.monotonic() + 10)
            self.assertEqual(set(api.call_args_list[0].args[1]), {"messages"})
