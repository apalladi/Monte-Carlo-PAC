import numpy as np


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


def simulate_multiple_investments(data, n_years, n_simulations):
    """
    Simulates multiple periodic investment strategies over random starting points.

    This function runs multiple simulations of a periodic investment strategy over
    historical stock data. It randomly selects starting points from the data and
    simulates the investment for the specified number of years, using the
    `simulate_single_investment` function. The goal is to generate a list of returns
    from different simulated investment scenarios.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing historical stock prices, where the first column represents
        the daily closing prices, and the index represents the dates.
    n_years : int
        The number of years over which to simulate each investment.
    n_simulations : int
        The number of investment simulations to run, each starting from a random point
        in the data.

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
        returns_list.append(simulate_single_investment(data, n_years, starting_point))

    return returns_list
