import unittest
import pandas as pd
import numpy as np
from src.data import import_data
from math import isclose
from src.simulations import (
    simulate_single_investment,
    simulate_multiple_investments,
    simulate_multiple_durations,
    simulate_portfolio_returns,
)


class TestSimulations(unittest.TestCase):
    def test_single_investment(self):
        interest = 5
        tax = 26
        df = pd.DataFrame(np.linspace(100, 100 + interest * 4, 1008), columns=["close"])

        final_return = simulate_single_investment(
            df, n_years=2, starting_point=5, verbose=False
        )

        self.assertTrue(isclose(final_return, interest * (1 - tax / 100), abs_tol=10 ** -1))

    def test_multiple_investments_single_asset(self):
        df = import_data("^GSPC", starting_date="2000-01-01")
        results = simulate_multiple_investments(df, n_years=10, n_simulations=10)

        self.assertEqual(
            len(results), 10, "The number of results does not match the number of simulations"
        )

    def test_multiple_investments_with_portfolio(self):
        # Simulated data: 1008 trading days (~4 years), prices for two assets
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),  # Simulated linear price increase
            "MSFT": np.linspace(50, 150, 1008),  # Simulated linear price increase
        })
        portfolio_composition = {
            "AAPL": 60,
            "MSFT": 40
        }
        results = simulate_multiple_investments(
            data=data,
            n_years=2,
            n_simulations=10,
            portfolio_composition=portfolio_composition
        )
        self.assertEqual(len(results), 10, "The number of results does not match the number of simulations")
        self.assertTrue(
            all(isinstance(result, float) for result in results),
            "All results should be floats"
        )

    def test_multiple_durations_single_asset(self):
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

    def test_multiple_durations_with_portfolio(self):
        # Simulated data: 1008 trading days (~4 years), prices for two assets
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),  # Simulated linear price increase
            "MSFT": np.linspace(50, 150, 1008),  # Simulated linear price increase
        })
        portfolio_composition = {
            "AAPL": 60,
            "MSFT": 40
        }
        years_grid = np.arange(1, 3.1, 1)

        results = simulate_multiple_durations(
            data=data,
            years_grid=years_grid,
            n_simulations=5,
            portfolio_composition=portfolio_composition
        )
        self.assertEqual(
            results.shape, (3, 5), "The shape must match the (number of periods, 5)"
        )
        self.assertTrue(
            all(results[:, 3] >= 0) and all(results[:, 4] >= 0),
            "All the probabilities must be larger than 0"
        )
        self.assertTrue(
            all(results[:, 3] <= 1) and all(results[:, 4] <= 1),
            "All the probabilities must be smaller than 1"
        )

    def test_portfolio_returns_correct_calculation(self):
        # Simulated data: 1008 trading days (~4 years), prices for two assets
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),  # Simulated linear price increase
            "MSFT": np.linspace(50, 150, 1008),  # Simulated linear price increase
        })
        portfolio_composition = {
            "AAPL": 60,
            "MSFT": 40
        }
        result = simulate_portfolio_returns(
            data=data,
            n_years=2,
            starting_point=5,
            portfolio_composition=portfolio_composition,
            verbose=False
        )
        self.assertIsInstance(result, float, "The return should be a float")
        self.assertGreaterEqual(result, 0, "Net return should be greater or equal to 0 for a rising price trend")

    def test_portfolio_invalid_sum(self):
        # Test case where the sum of portfolio percentages is not 100
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),
            "MSFT": np.linspace(50, 150, 1008),
        })
        invalid_portfolio = {
            "AAPL": 50,
            "MSFT": 30
        }
        with self.assertRaises(ValueError):
            simulate_portfolio_returns(
                data=data,
                n_years=2,
                starting_point=5,
                portfolio_composition=invalid_portfolio
            )

    def test_portfolio_missing_ticker(self):
        # Test case where the portfolio references a missing ticker
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),
            "MSFT": np.linspace(50, 150, 1008),
        })
        invalid_portfolio = {
            "AAPL": 60,
            "GOOGL": 40  # GOOGL is not in the data
        }
        with self.assertRaises(KeyError):
            simulate_portfolio_returns(
                data=data,
                n_years=2,
                starting_point=5,
                portfolio_composition=invalid_portfolio
            )

    def test_portfolio_verbose_output(self):
        # Test case to check verbose output (visual inspection)
        data = pd.DataFrame({
            "AAPL": np.linspace(100, 200, 1008),
            "MSFT": np.linspace(50, 150, 1008),
        })
        portfolio_composition = {
            "AAPL": 60,
            "MSFT": 40
        }
        result = simulate_portfolio_returns(
            data=data,
            n_years=2,
            starting_point=5,
            portfolio_composition=portfolio_composition,
            verbose=True  # Prints output
        )
        self.assertIsInstance(result, float, "The return should be a float")


if __name__ == "__main__":
    unittest.main()
