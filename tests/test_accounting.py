"""Missing measurements must not manufacture known zero compute."""

import unittest

from efficient_agentic_inference.evaluation import observed_sum


class AccountingContracts(unittest.TestCase):
    def test_cpu_observations_distinguish_unknown_zero_and_partial(self):
        self.assertIsNone(observed_sum([None, None]))
        self.assertIsNone(observed_sum([]))
        self.assertEqual(observed_sum([0, None]), 0)
        self.assertEqual(observed_sum([2.5, None, 3.5]), 6)
