import unittest
from src.stats import compute_summary_stats


class TestComputeSummaryStats(unittest.TestCase):
    def test_normal_returns(self):
        # Test case 1: Normal returns
        returns = [1.0, 2.5, -0.5, 3.0, 4.0]
        expected_output = (
            -0.5,
            4.0,
            2.5,
            0.8,
            0.6,
        )  # Expected stats: (min, max, median, prob_non_negative, prob_greater_than_inflation)

        result = compute_summary_stats(returns)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_all_positive_returns(self):
        # Test case 2: All positive returns
        returns = [1.9, 3.5, 5.0, 4.0, 1.5]
        expected_output = (1.5, 5.0, 3.5, 1.0, 0.6)

        result = compute_summary_stats(returns)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_all_negative_returns(self):
        # Test case 3: All negative returns
        returns = [-1.0, -2.5, -0.5, -3.0, -4.0]
        expected_output = (-4.0, -0.5, -2.5, 0.0, 0.0)

        result = compute_summary_stats(returns)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_mixed_returns_with_thresholds(self):
        # Test case 4: Mixed returns with some exactly at the thresholds
        returns = [0.0, 2.0, 2.0, 3.0, -1.0]
        expected_output = (-1.0, 3.0, 2.0, 0.6, 0.2)

        result = compute_summary_stats(returns)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")


if __name__ == "__main__":
    unittest.main()
