"""Independently specified four-arm failure/primary analysis invariants."""

import copy
import unittest

from efficient_agentic_inference.reliability import ARMS, reliability_summary


def row(instance_id, valid, recall, strict):
    return {
        "instance_id": instance_id,
        "disposition": "valid" if valid else "invalid_output",
        "all_files": {
            "gold_file_count": 2,
            "candidate_recall_ceiling": 1.0,
            "recall_at_k": {"5": recall},
            "strict_success_at_k": {"5": strict},
        },
    }


class ReliabilityContracts(unittest.TestCase):
    def fixture(self):
        free = [row("a", False, 0.0, False), row("b", True, 0.5, False)]
        constrained = [row("a", True, 1.0, True), row("b", True, 0.5, False)]
        return {
            "S-free": free,
            "S-constrained": constrained,
            "G-free": copy.deepcopy(constrained),
            "G-constrained": copy.deepcopy(free),
        }

    def test_all_attempts_and_single_primary_remain_in_comparison(self):
        result = reliability_summary(self.fixture(), {"a": "repo", "b": "repo"})
        small, large = result["contrasts"]["S"], result["contrasts"]["G"]
        self.assertEqual(small["selected"], 2)
        self.assertEqual(small["recall_at_5_gain"], 0.5)
        self.assertTrue(small["numerical_signal_rule_pass"])
        self.assertEqual(small["valid_free"], 1)
        self.assertEqual(small["valid_constrained"], 2)
        self.assertEqual(small["validity_discordance"]["free_invalid_constrained_valid"], 1)
        self.assertEqual(large["recall_at_5_gain"], -0.5)
        self.assertEqual(large["validity_discordance"]["free_valid_constrained_invalid"], 1)
        self.assertNotIn("numerical_signal_rule_pass", large)
        self.assertEqual(result["interaction_recall_at_5_point_estimate"], -1.0)

    def test_mismatch_unknown_or_repaired_failure_blocks_analysis(self):
        for arm in ARMS:
            for field in ("gold_file_count", "candidate_recall_ceiling"):
                arms = copy.deepcopy(self.fixture())
                arms[arm][0]["all_files"][field] = 7
                with self.assertRaises(ValueError):
                    reliability_summary(arms, {"a": "repo", "b": "repo"})
        arms = self.fixture()
        arms["S-free"][0]["all_files"]["recall_at_k"]["5"] = 0.5
        with self.assertRaisesRegex(ValueError, "zero quality"):
            reliability_summary(arms, {"a": "repo", "b": "repo"})
        arms["S-free"][0]["all_files"]["recall_at_k"]["5"] = None
        with self.assertRaises(ValueError):
            reliability_summary(arms, {"a": "repo", "b": "repo"})
