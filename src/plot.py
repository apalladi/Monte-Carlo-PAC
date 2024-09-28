"""
This module provides a function for visualizing investment simulation results.

It generates plots that illustrate the median return and the probability of
positive returns over various investment durations.

Function:
---------
- show_results: Plots simulation results, optionally saving the figure.
"""

import matplotlib.pyplot as plt
import numpy as np


def show_results(years_grid, results, title, save_figure=False):
    """
    Visualizes and compares the results of simulated investment returns over multiple durations.

    This function generates two subplots:
    1. The median yearly net return for each duration (from `years_grid`),
    along with a shaded region representing the range of
    all simulated returns (min to max) over 1000 simulations.
    2. The probability of achieving a positive nominal net return, as well as the probability of
       achieving a positive real net return, accounting for a 2% inflation rate.

    The function optionally saves the figure to a file
    if `save_figure` is provided as a string (filename).

    Parameters:
    -----------
    years_grid : array-like
        A list or array of investment durations in years.
    results : numpy.ndarray
        A 2D array where each row corresponds to the summary statistics for a specific duration.
        - results[:, 0]: Minimum return across simulations.
        - results[:, 1]: Maximum return across simulations.
        - results[:, 2]: Median return across simulations.
        - results[:, 3]: Probability of positive net nominal return.
        - results[:, 4]: Probability of positive net real return (accounting for 2% inflation).
    title : str
        The title of the plot displayed at the top of the figure.
    save_figure : bool or str, optional (default=False)
        - If False, the plot is not saved to a file.
        - If a string (filename), the plot will be saved as an image file with the given filename.
        - Raises a ValueError if the argument is neither False nor a string.

    Returns:
    --------
    None
        This function does not return any values.
        It displays the plots and optionally saves them to a file.

    Notes:
    ------
    The function also includes a small credit to Dr. Andrea Palladino at the bottom of the figure.
    """

    fig = plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(years_grid[1:], results[1:, 2], label="median return")
    plt.fill_between(
        years_grid[1:],
        results[1:, 1],
        results[1:, 0],
        alpha=0.5,
        label="returns of all simulations \n(1000 sim. for each duration)",
    )
    plt.grid()
    plt.ylabel("Yearly net return")
    plt.title("Returns of PAC")
    plt.legend()
    plt.xlabel("Duration of PAC (years)")

    plt.subplot(1, 2, 2)
    plt.plot(
        np.concatenate([[0], years_grid]),
        np.concatenate([[0], results[:, 3]]),
        color="C2",
        label="Nominal return",
    )
    plt.plot(
        np.concatenate([[0], years_grid]),
        np.concatenate([[0], results[:, 4]]),
        color="C1",
        label="Real return accounting for 2% inflation",
    )
    plt.grid()
    plt.ylabel("Probabily of positive net return")
    plt.legend()
    plt.xlabel("Duration of PAC (years)")
    plt.title("Probabily of positive net return")

    plt.tight_layout()
    fig.text(0.42, 0.02, "Credit: Dr. Andrea Palladino", color="darkslategrey")
    fig.text(0.25, 1.01, title, color="darkblue", weight="bold")

    if isinstance(save_figure, bool) and save_figure is False:
        pass
    elif isinstance(save_figure, str):
        plt.savefig(save_figure, dpi=300, bbox_inches="tight")
    else:
        raise ValueError("save_figure can be False or equal to a string")

    plt.show()
