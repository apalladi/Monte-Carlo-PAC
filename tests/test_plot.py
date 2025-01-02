import os
import unittest
import numpy as np
from src.data import import_data
from src.simulations import simulate_multiple_durations
from src.plot import show_results


class TestShowResults(unittest.TestCase):
    def test_show_results(self):
        # Import data
        df = import_data("^GSPC", starting_date="2000-01-01")
        years_grid = np.arange(1, 10.1, 1)

        # Simulate multiple durations
        results = simulate_multiple_durations(
            data=df, years_grid=years_grid, n_simulations=10
        )

        # Generate and save the figure
        save_path = "results/test-figure.png"
        show_results(
            years_grid,
            results,
            title="test figure",
            show_figure=False,
            save_figure=save_path,
        )

        # Check if the file exists
        self.assertTrue(os.path.exists(save_path), "The file has not been created. Check show_results function")

        # Cleanup the test file
        os.remove(save_path)


if __name__ == "__main__":
    unittest.main()
