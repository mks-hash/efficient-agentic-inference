"""Independent score-format invariants; fixtures establish no model quality."""

import copy
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import test_llama_predict as legacy
from jsonschema import Draft202012Validator

from efficient_agentic_inference.llama_predict import (
    candidate_score_ranking,
    candidate_score_schema,
    classify,
    infer,
)
from efficient_agentic_inference.records import digest, encoded


class ScoreRankingContracts(unittest.TestCase):
    def test_scores_bind_once_and_ties_have_a_gold_blind_order(self):
        paths = ["a.py", "b.py", "c.py", "d.py", "e.py"]
        self.assertEqual(
            candidate_score_ranking([0, 75, 100, 75, 0], paths), ["c.py", "b.py", "d.py"]
        )
        self.assertEqual(candidate_score_ranking([0] * 5, paths), [])
        self.assertEqual(candidate_score_ranking([], []), [])
        many = [f"src/{i:02}.py" for i in range(20)]
        self.assertEqual(candidate_score_ranking([50] * 20, many), many[:10])
        self.assertEqual(candidate_score_ranking(list(range(20)), many), list(reversed(many))[:10])

    def test_partial_coerced_or_path_answers_never_become_valid_scores(self):
        for raw in (
            [1],
            [1, 2, 3],
            [True, 1],
            [1.0, 2],
            ["1", 2],
            [-1, 0],
            [101, 0],
            [None, 0],
            {"scores": [1, 2]},
            ["a.py", "a.py"],
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                candidate_score_ranking(raw, ["a.py", "b.py"])
        for paths in (
            ["b.py", "a.py"],
            ["a.py", "a.py"],
            ["../bad.py"],
            [f"{i:02}.py" for i in range(21)],
        ):
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                candidate_score_schema(paths)

    def test_schema_has_exact_candidate_count_and_finite_integer_domain(self):
        schema = candidate_score_schema(["a.py", "b.py"])
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        self.assertTrue(validator.is_valid([0, 100]))
        self.assertTrue(validator.is_valid([37, 37]))
        for raw in ([], [1], [1, 2, 3], [-1, 1], [101, 1], [True, 1]):
            self.assertFalse(validator.is_valid(raw))
        self.assertEqual(schema["minItems"], 2)
        self.assertEqual(schema["maxItems"], 2)
        self.assertNotIn("uniqueItems", schema)

    def test_classification_requires_native_provenance_and_exact_binding(self):
        config = {**legacy.CONFIG, "output_constraint": {"policy": "candidate-score-vector-v1"}}
        saved = legacy.evidence()
        paths = ["a.py", "b.py"]
        saved.update(
            raw_output="[25,100]",
            score_binding=paths,
            score_binding_sha256=digest(encoded(paths)),
            request={"json_schema": candidate_score_schema(paths)},
        )
        saved["final_response"]["generation_settings"].update(
            grammar='root ::= "[]"', grammar_lazy=False
        )
        self.assertEqual(classify(saved, set(paths), config), ["b.py", "a.py"])
        for key, value in (
            ("score_binding", list(reversed(paths))),
            ("score_binding_sha256", "0" * 64),
            ("request", {"json_schema": candidate_score_schema(["a.py"])}),
        ):
            bad = copy.deepcopy(saved)
            bad[key] = value
            with self.assertRaisesRegex(ValueError, "binding_or_schema"):
                classify(bad, set(paths), config)
        saved["raw_output"] = "[25,100.0]"
        with self.assertRaisesRegex(ValueError, "integers"):
            classify(saved, set(paths), config)
        saved["raw_output"] = "[25,100]"
        saved["final_response"]["stop_type"] = "limit"
        with self.assertRaisesRegex(ValueError, "completion_stop"):
            classify(saved, set(paths), config)

    def test_inference_emits_binding_and_retains_score_text_without_repair(self):
        config = {**legacy.CONFIG, "output_constraint": {"policy": "candidate-score-vector-v1"}}

        def complete(payload, deadline, saved, trace):
            saved["output_token_ids"] = [20, 21]
            saved["raw_output"] = "[100]"
            saved["final_response"] = legacy.evidence()["final_response"]
            saved["final_response"]["generation_settings"].update(
                grammar='root ::= "[100]"', grammar_lazy=False
            )

        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            with (
                patch(
                    "efficient_agentic_inference.llama_predict.post",
                    side_effect=[{"prompt": "native"}, {"tokens": [101, 102]}],
                ),
                patch("efficient_agentic_inference.llama_predict.stream", side_effect=complete),
            ):
                prediction = infer(
                    legacy.ModelEvidenceContracts().task(),
                    config,
                    "score prompt",
                    folder,
                    time.monotonic() + 10,
                )
            self.assertEqual(prediction["disposition"], "valid")
            self.assertEqual(prediction["ranked_files"], ["src/a.py"])
            self.assertEqual(prediction["raw_output"], "[100]")
            saved = json.loads((folder / "evidence.json").read_text())
            self.assertEqual(saved["score_binding"], ["src/a.py"])
            self.assertEqual(saved["request"]["json_schema"]["minItems"], 1)
