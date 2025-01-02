import unittest
import pandas as pd
import numpy as np
from src.data import import_data
from math import isclose
from src.simulations import simulate_single_investment, simulate_multiple_investments, simulate_multiple_durations


class TestSimulations(unittest.TestCase):
    def test_single_investment(self):
        interest = 5
        tax = 26
        df = pd.DataFrame(np.linspace(100, 100 + interest * 4, 1008), columns=["close"])

        final_return = simulate_single_investment(
            df, n_years=2, starting_point=5, verbose=False
        )

        self.assertTrue(
            isclose(final_return, interest * (1 - tax / 100), abs_tol=10 ** -1))

    def test_multiple_investments(self):
        df = import_data("^GSPC", starting_date="2000-01-01")
        results = simulate_multiple_investments(df, n_years=10, n_simulations=10)

        self.assertEqual(
            len(results), 10, "The number of results does not match the number of simulations"
        )

    def test_multiple_durations(self):
        df = import_data("^GSPC", starting_date="2000-01-01")
        years_grid = np.arange(1, 10.1, 1)

        results = simulate_multiple_durations(df, years_grid=years_grid, n_simulations=10)

        self.assertEqual(
            results.shape, (10, 5), "The shape must match the (number of periods, 5)"
        )
        self.assertTrue(
            all(results[:, 3] >= 0) and all(results[:, 4] >= 0),
            "All the probabilities must be larger than 0"
        )
        self.assertTrue(
            all(results[:, 3] <= 1) and all(results[:, 4] <= 1),
            "All the probabilities must be smaller than 1"
        )


if __name__ == "__main__":
    unittest.main()
