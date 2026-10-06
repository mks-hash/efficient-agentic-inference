"""Independently specified denominators and missing-cost examples; synthetic only."""

import copy
import json
import unittest
from pathlib import Path

import jsonschema

from efficient_agentic_inference.accounting import cost_summary

SCHEMA = json.loads(
    (Path(__file__).parents[1] / "schemas/accounting/v1/ledger.schema.json").read_text()
)


def fixture():
    ledger = {
        "schema_version": "1.0.0",
        "synthetic": True,
        "boundary": "localization-batch-v1",
        "treatment": "synthetic",
        "selected": 4,
        "currency": "USD",
        "allocation_policy": "Synthetic four-task standalone batch; includes two failures",
        "components": [
            {
                "name": name,
                "actual_usd": value,
                "actual_evidence": "Synthetic independently specified charge/absence",
                "scenario_usd": value,
                "scenario_basis": "Synthetic assumption",
            }
            for name, value in (
                ("compute", 0.8),
                ("storage", 0.2),
                ("external_ip", 0),
                ("network", 0),
                ("external_preparation", 0.2),
                ("other", 0),
            )
        ],
    }
    evaluation = {
        "synthetic": True,
        "selected": 4,
        "all_files": {"strict_successes_at_5": 2, "unknown_label_tasks": 0},
    }
    return ledger, evaluation


class CostLedgerContracts(unittest.TestCase):
    def test_failures_remain_in_cost_and_population(self):
        ledger, evaluation = fixture()
        result = cost_summary(ledger, evaluation, SCHEMA)
        self.assertEqual(result["actual"]["total_usd"], 1.2)
        self.assertEqual(result["actual"]["cost_per_success_usd"], 0.6)
        self.assertEqual(result["selected"], 4)
        self.assertEqual(result["failed_or_unsuccessful_tasks"], 2)
        self.assertTrue(result["synthetic"])
        evaluation["selected"] = 3
        with self.assertRaises(ValueError):
            cost_summary(ledger, evaluation, SCHEMA)

    def test_synthetic_cost_cannot_be_joined_to_measured_evaluation(self):
        ledger, evaluation = fixture()
        evaluation["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "Synthetic"):
            cost_summary(ledger, evaluation, SCHEMA)

    def test_scenario_cannot_fill_unknown_actual_or_omit_component(self):
        ledger, evaluation = fixture()
        ledger["components"][0]["actual_usd"] = None
        result = cost_summary(ledger, evaluation, SCHEMA)
        self.assertIsNone(result["actual"]["total_usd"])
        self.assertIsNone(result["actual"]["cost_per_success_usd"])
        self.assertEqual(result["scenario"]["cost_per_success_usd"], 0.6)
        ledger["components"][-1] = copy.deepcopy(ledger["components"][0])
        with self.assertRaises(ValueError):
            cost_summary(ledger, evaluation, SCHEMA)

    def test_zero_and_unknown_denominators_remain_distinct(self):
        ledger, evaluation = fixture()
        evaluation["all_files"]["strict_successes_at_5"] = 0
        result = cost_summary(ledger, evaluation, SCHEMA)
        self.assertEqual(result["actual"]["cps_status"], "UNDEFINED_ZERO_SUCCESSES")
        self.assertIsNone(result["actual"]["cost_per_success_usd"])
        evaluation["all_files"]["unknown_label_tasks"] = 1
        result = cost_summary(ledger, evaluation, SCHEMA)
        self.assertEqual(result["actual"]["cps_status"], "UNKNOWN_LABELS")
        self.assertEqual(result["success_denominator_status"], "UNKNOWN")

    def test_known_zero_needs_evidence_and_nonfinite_cost_rejected(self):
        ledger, evaluation = fixture()
        ledger["components"][-1]["actual_evidence"] = None
        with self.assertRaises(jsonschema.ValidationError):
            cost_summary(ledger, evaluation, SCHEMA)
        ledger, evaluation = fixture()
        ledger["components"][0]["scenario_usd"] = float("nan")
        with self.assertRaises(ValueError):
            cost_summary(ledger, evaluation, SCHEMA)
