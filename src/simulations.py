"""
Investment Simulation Module

This module provides functionality to simulate periodic investment strategies
and compute summary statistics based on historical stock data. It includes
functions to simulate single or multiple investments over a given time period
and compute the resulting returns. Additionally, it supports running simulations
across various investment durations and summarizing the outcomes.

Functions:
----------
simulate_single_investment(data, n_years, starting_point, verbose=False):
    Simulates a single periodic investment strategy over a specified number of years.

simulate_multiple_investments(data, n_years, n_simulations):
    Runs multiple investment simulations with different starting points and
    returns a list of annualized net returns.

simulate_multiple_durations(data, years_grid, n_simulations):
    Simulates investments for a range of durations and computes summary statistics
    for each duration based on multiple simulations.

Dependencies:
-------------
- numpy (imported as np): Used for numerical operations.
- tqdm: Used to show progress bars during simulations.
- src.stats.compute_summary_stats: A custom function for calculating summary statistics
  from simulated returns.
"""

import numpy as np
from tqdm import tqdm
from src.stats import compute_summary_stats


def simulate_single_investment(data, n_years, starting_point, verbose=False):
    """
    Simulates a periodic investment strategy in a stock over a specified time period.

    This function models a scenario where a fixed amount of capital (100€) is invested
    every 21 trading days in a stock over a specified number of years. It calculates
    the gross and net return based on the stock's price fluctuations, assuming a flat
    capital addition every period, and applies a 26% tax on positive returns.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing historical stock prices, where the first column represents
        the daily closing prices, and the index represents the dates.
    n_years : int
        The number of years over which to simulate the investment.
    starting_point : int
        The index of the starting day in the `data` DataFrame from which the simulation begins.
    verbose : bool, optional (default=False)
        If True, prints detailed output of the simulation, including the final capital,
        final investment value, gross return, net return, and annualized net return.

    Returns:
    --------
    float
        The annualized net return of the investment over the simulated period,
        expressed as a percentage.
    """
    final_point = starting_point + int(252 * n_years)

    initial_price = data.iloc[starting_point, 0]
    capital = 100
    n_stocks = 100 / initial_price

    for i in np.arange(starting_point + 21, final_point, 21):
        capital += 100
        new_price = data.iloc[i, 0]
        n_stocks += 100 / new_price

    final_price = data.iloc[final_point, 0]
    final_value = n_stocks * final_price
    average_capital = capital / 2

    gross_return = (final_value - capital) / average_capital * 100

    if gross_return > 0:
        net_return = 0.74 * gross_return
    else:
        net_return = gross_return

    net_return_per_year = 100 * ((1 + net_return / 100) ** (1 / n_years) - 1)

    if verbose:
        print("final capital", int(capital), "€")
        print("final value", int(final_value), "€")
        print("gross return", round(gross_return, 2), "%")
        print("net return", round(net_return, 2), "%")
        print("net return per year", round(net_return_per_year, 2), "%")

    return net_return_per_year


def simulate_multiple_investments(data, n_years, n_simulations, portfolio_composition=None):
    """
    Simulates multiple periodic investment strategies over random starting points.

    This function runs multiple simulations of a periodic investment strategy over
    historical stock data. If `portfolio_composition` is provided, it simulates the
    investment using `simulate_portfolio_returns`, considering the composition of the portfolio.
    Otherwise, it defaults to using `simulate_single_investment` for each simulation.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing historical stock prices, where the first column represents
        the daily closing prices (if `simulate_single_investment` is used), or multiple columns
        represent asset prices (if `simulate_portfolio_returns` is used).
    n_years : int
        The number of years over which to simulate each investment.
    n_simulations : int
        The number of investment simulations to run, each starting from a random point
        in the data.
    portfolio_composition : dict, optional
        A dictionary where keys are ticker names (columns in `data`) and values are percentages
        (as integers) representing the composition of the portfolio.
        If not provided, the simulation defaults to `simulate_single_investment`.

    Returns:
    --------
    list
        A list of annualized net returns for each simulation, where each entry is
        the result of a single simulated investment over `n_years`.
    """
    if n_simulations > len(data) / 2:
        print(
            "WARNING: the number of simulation is too high compared to \
        the dimension of the time-series"
        )
        print("The suggested number of simulation is", int(len(data) / 2))

    max_final_point = len(data) - int(252 * n_years)
    extracted_starting_points = np.random.choice(
        np.arange(0, max_final_point), size=n_simulations, replace=False
    )
    returns_list = []

    for starting_point in extracted_starting_points:
        if portfolio_composition is not None:
            # Use portfolio simulation if composition is provided
            returns_list.append(
                simulate_portfolio_returns(data, n_years, starting_point, portfolio_composition)
            )
        else:
            # Default to single investment simulation
            returns_list.append(simulate_single_investment(data, n_years, starting_point))

    return returns_list


def simulate_multiple_durations(data, years_grid, n_simulations, portfolio_composition=None):
    """
    Simulates periodic investments across multiple investment durations
    and computes summary statistics.

    This function runs multiple investment simulations for each duration specified in `years_grid`.
    For each duration, it performs `n_simulations` using the `simulate_multiple_investments` function,
    optionally taking into account a specified portfolio composition.
    Then, it computes summary statistics for the resulting returns
    using the `compute_summary_stats` function.
    The results are stored as an array of summary statistics for each investment duration.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing historical stock prices, where the first column represents the daily
        closing prices (if `portfolio_composition` is None), or multiple columns representing
        asset prices if using a portfolio.
    years_grid : list or array-like
        A list or array specifying the different durations (in years)
        over which to simulate the investments.
    n_simulations : int
        The number of investment simulations to run for each duration in `years_grid`.
    portfolio_composition : dict, optional
        A dictionary where keys are ticker names (columns in `data`) and values are percentages
        (as integers) representing the composition of the portfolio. The percentages must sum to 100.
        If not provided, the simulation defaults to single investments.

    Returns:
    --------
    numpy.ndarray
        An array where each element contains the summary statistics
        for a particular duration in `years_grid`.
        Each element is the result of applying `compute_summary_stats` on the simulated returns.

    Example:
    --------
    >>> portfolio = {"VTI": 80, "BND": 20}
    >>> years_grid = [5, 10, 15]
    >>> simulate_multiple_durations(tickers_data, years_grid, 100, portfolio)
    array([[min_return, max_return, median_return, prob_non_negative, prob_greater_than_inflation],
           [min_return, max_return, median_return, prob_non_negative, prob_greater_than_inflation],
           [min_return, max_return, median_return, prob_non_negative, prob_greater_than_inflation]])
    """
    summary_results = []

    for i in tqdm(range(len(years_grid))):
        returns_list = simulate_multiple_investments(
            data, years_grid[i], n_simulations, portfolio_composition
        )
        summary_results.append(compute_summary_stats(returns_list))

    return np.array(summary_results)


def simulate_portfolio_returns(data, n_years, starting_point, portfolio_composition, verbose=False):
    """
    Simulates a periodic investment strategy in a stock over a specified time period.

    This function models a scenario where a fixed amount of capital is invested every 21
    trading days (e.g. 252 trading days over 12 months) in a portfolio of assets over a
    specified number of years. It calculates the gross and net return based on the stock's
    price fluctuations, assuming a flat capital addition every period, and applies a fixed
    tax on positive returns.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing historical stock prices, where each column represents a ticker,
        and the rows represent daily closing prices.
    n_years : int
        The number of years over which to simulate the investment.
    starting_point : int
        The index of the starting day in the `data` DataFrame from which the simulation begins.
    portfolio_composition : dict
        A dictionary where keys are ticker names (columns in `data`) and values are percentages
        (as integers) representing the composition of the portfolio.
    verbose : bool, optional (default=False)
        If True, prints detailed output of the simulation, including the final capital,
        final investment value, gross return, net return, and annualized net return.

    Returns:
    --------
    float
        The annualized net return of the portfolio over the simulated period, expressed as a percentage.
    """
    # Fixed constants
    TAX_RATE = 0.26  # Tax rate on positive returns (TODO this may be handled differently)
    MONTHLY_CONTRIBUTION = 100  # Fixed amount invested each month

    # Validate portfolio composition
    if sum(portfolio_composition.values()) != 100:
        raise ValueError("The sum of the percentages in 'portfolio_composition' must be equal to 100.")

    # Validate data
    for ticker in portfolio_composition.keys():
        if ticker not in data.columns:
            raise KeyError(f"Ticker '{ticker}' is not found in the data columns.")

    # Simulation parameters
    final_point = starting_point + int(252 * n_years)
    trading_period_days = 21  # buying interval (in days)

    # Initial conditions
    total_capital = 0
    total_value = 0
    average_capital = 0

    for ticker, percentage in portfolio_composition.items():
        capital = 0
        n_stocks = 0
        allocation = MONTHLY_CONTRIBUTION * (percentage / 100)  # distributed accordingly

        for i in np.arange(starting_point, final_point, trading_period_days):
            capital += allocation
            price = data.loc[data.index[i], ticker]
            n_stocks += allocation / price  # the number of stocks bought in the current period
            average_capital += allocation / 2  # adding half of the contribution for average capital

        final_price = data.loc[data.index[final_point], ticker]
        final_value = n_stocks * final_price
        total_capital += capital
        total_value += final_value

    gross_return = (total_value - total_capital) / average_capital * 100

    # Apply taxation only to positive returns
    if gross_return > 0:
        net_return = (1 - TAX_RATE) * gross_return
    else:
        net_return = gross_return

    net_return_per_year = 100 * ((1 + net_return / 100) ** (1 / n_years) - 1)

    if verbose:
        print("Total capital invested:", int(total_capital), "€")
        print("Final portfolio value:", int(total_value), "€")
        print("Gross return:", round(gross_return, 2), "%")
        print("Net return:", round(net_return, 2), "%")
        print("Net return per year:", round(net_return_per_year, 2), "%")

    return net_return_per_year
