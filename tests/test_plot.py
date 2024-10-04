import os
import numpy as np
from src.data import import_data
from src.simulations import simulate_multiple_durations
from src.plot import show_results


def test_show_results():
    df = import_data("^GSPC", starting_date="2000-01-01")
    years_grid = np.arange(1, 10.1, 1)

    results = simulate_multiple_durations(
        data=df, years_grid=years_grid, n_simulations=10
    )

    show_results(
        years_grid,
        results,
        title="test figure",
        show_figure=False,
        save_figure="results/test-figure.png",
    )

    condition = os.path.exists("results/test-figure.png") == True

    assert condition, "The file has not been created. Check show_results function"

    os.remove("results/test-figure.png")
