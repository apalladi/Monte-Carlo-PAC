"""
This module provides functions to retrieve and process historical stock price data
from Yahoo Finance.

The module includes two primary functions:
1. `import_data`: Retrieves historical daily closing prices for a specific stock ticker.
2. `generate_df_from_list`: Generates a DataFrame of historical closing prices
for multiple stock tickers.

Both functions rely on Yahoo Finance as the data source and use `pandas` for data manipulation.
The data can be fetched starting from a given date up to the current date. The resulting DataFrames
are indexed by date and contain only the closing price for each stock ticker.

Functions:
----------
import_data(ticker, starting_date):
    Retrieves historical closing prices for a specific stock ticker.

generate_df_from_list(list_tickers, starting_time):
    Retrieves and combines historical closing prices for a list of stock tickers
    into a single DataFrame.

Example usage:
--------------
# Import historical data for Apple and Microsoft starting from January 1, 2020
df = generate_df_from_list(['AAPL', 'MSFT'], '2020-01-01')
print(df.head())
"""

import datetime as dt
import yfinance as yfin
from pandas_datareader import data as pdr


def import_data(ticker, starting_date):
    """
    Import historical stock price data from Yahoo Finance for a given ticker.

    This function retrieves historical daily closing price data for a specified stock ticker
    from Yahoo Finance using the `yfinance` and `pandas_datareader` libraries. It fetches data
    starting from the provided date up to the current date. The resulting DataFrame contains only
    the closing prices.

    Parameters:
    -----------
    ticker : str
        The stock ticker symbol (e.g., "AAPL" for Apple).
    starting_date : str or datetime
        The starting date for the data retrieval in string format (YYYY-MM-DD)
        or as a datetime object.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame indexed by date, containing one column labeled with the ticker symbol
        and the stock's daily closing prices.

    Example:
    --------
    >>> import_data('AAPL', '2020-01-01')
            AAPL
    Date
    2020-01-02   297.43
    2020-01-03   293.65
    2020-01-06   299.80
    ...
    """
    end = dt.datetime.now()
    yfin.pdr_override()
    data = pdr.get_data_yahoo(ticker, start=starting_date, end=end)
    data.reset_index(inplace=True)
    data.set_index("Date", inplace=True)
    data = data.drop(["Low", "Open", "Adj Close", "High", "Volume"], axis="columns")
    data.columns = [str(ticker)]
    return data


def generate_df_from_list(list_tickers, starting_date):
    """
    Generate a DataFrame with historical closing price data for a list of stock tickers.

    This function retrieves historical daily closing price data for multiple stock tickers
    from Yahoo Finance, starting from the specified date. It combines the data into a single
    DataFrame, where each column corresponds to a stock ticker. Missing data is forward-filled
    to handle gaps.

    Parameters:
    -----------
    list_tickers : list of str
        A list of stock ticker symbols (e.g., ["AAPL", "MSFT"]).
    starting_date : str or datetime
        The starting date for data retrieval, in string format (YYYY-MM-DD) or as a datetime object.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing historical closing prices for each ticker in the `list_tickers`,
        with each column labeled by the ticker symbol. Rows are indexed by date, and the data
        includes only entries from the `starting_time` onward.

    Example:
    --------
    >>> generate_df_from_list(['AAPL', 'MSFT'], '2020-01-01')
                AAPL     MSFT
    Date
    2020-01-02   297.43   160.62
    2020-01-03   293.65   158.96
    2020-01-06   299.80   159.03
    ...
    """
    for i, ticker in enumerate(list_tickers):
        if i == 0:
            data = import_data(ticker, starting_date)
        else:
            new_data = import_data(ticker, starting_date)
            data = data.join(new_data, on=data.index)

    data.fillna(inplace=True, method="ffill")
    data.columns = list_tickers

    data = data[data.index >= starting_date]

    return data
