import pandas as pd
import numpy as np
from src.data import import_data
from src.simulations import *
from math import isclose


def test_single_investment():

    interest = 5
    tax = 26
    df = pd.DataFrame(np.linspace(100, 100 + interest * 4, 1008), columns=["close"])

    final_return = simulate_single_investment(
        df, n_years=2, starting_point=5, verbose=False
    )

    assert isclose(final_return, interest * (1 - tax / 100), abs_tol=10 ** -1)


def test_multiple_investments():
    df = import_data("^GSPC", starting_date="2000-01-01")
    results = simulate_multiple_investments(df, n_years=10, n_simulations=10)

    assert (
        len(results) == 10
    ), "The number of results does not match the number of simulations"


def test_multiple_durations():
    df = import_data("^GSPC", starting_date="2000-01-01")
    years_grid = np.arange(1, 10.1, 1)

    results = simulate_multiple_durations(df, years_grid=years_grid, n_simulations=10)

    assert results.shape == (10, 5), "The shape must match the (number of periods, 5)"
    assert all(results[:, 3] >= 0) & all(
        results[:, 4] >= 0
    ), "All the probabilities must be larger than 0"
    assert all(results[:, 3] <= 1) & all(
        results[:, 4] <= 1
    ), "All the probabilities must be smaller than 1"


if __name__ == "__main__":
    test_single_investment()
    test_multiple_investments()
    test_multiple_durations()
