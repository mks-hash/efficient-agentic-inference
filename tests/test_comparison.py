"""Repository-block pairing differs from independent task resampling."""

import copy
import unittest

from efficient_agentic_inference.comparison import paired_comparison


def record(name, recall):
    return {
        "instance_id": name,
        "all_files": {
            "recall_at_k": {"5": recall},
            "gold_file_count": 1,
            "candidate_recall_ceiling": 1,
            "strict_success_at_k": {"5": recall == 1},
        },
    }


class PairedContracts(unittest.TestCase):
    def test_cluster_membership_and_paired_constant_gain(self):
        control = [record("a", 0), record("b", 0), record("c", 0)]
        model = [record("a", 1), record("b", 1), record("c", 1)]
        repositories = {"a": "repo1", "b": "repo1", "c": "repo2"}
        result = paired_comparison(model, control, repositories)
        self.assertEqual(result["recall_at_5_gain"], 1)
        self.assertEqual(result["paired_repo_bootstrap_95_ci"], [1, 1])
        self.assertEqual(result["repository_blocks"], 2)
        self.assertTrue(result["decision_rule_pass"])
        self.assertEqual(paired_comparison(model[::-1], control, repositories), result)
        negative = paired_comparison(control, model, repositories)
        self.assertEqual(negative["paired_repo_bootstrap_95_ci"], [-1, -1])
        self.assertFalse(negative["decision_rule_pass"])

    def test_missing_pair_or_unknown_score_cannot_be_dropped(self):
        left = [record("a", 1)]
        with self.assertRaises(ValueError):
            paired_comparison(left, [record("b", 0)], {"a": "repo"})
        unknown = copy.deepcopy(left)
        unknown[0]["all_files"]["recall_at_k"]["5"] = None
        with self.assertRaises(ValueError):
            paired_comparison(unknown, left, {"a": "repo"})
        with self.assertRaises(ValueError):
            paired_comparison(left * 2, left, {"a": "repo"})
