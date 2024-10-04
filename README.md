# Monte-Carlo PAC, Capital Accumulation Plan

## Introduction
This repository provides a tool to simulate investments of varying durations across different types of assets using **Monte Carlo simulations**. The assets can include **stocks, ETFs, bond ETFs**, or **market indices** such as the **S&P 500**. The simulation specifically refers to a **monthly investment of a fixed amount of money** rather than a one-time investment. It strictly analyzes past data to produce a distribution of returns based on historical performance, without any predictive power regarding future outcomes.

The goal is to obtain the return distribution for different investment durations, allowing users to assess the likelihood of achieving positive returns, both in nominal terms and in real terms (adjusted for inflation). This method can help investors gain insights into how various assets have performed historically over time, but it should not be interpreted as a tool for forecasting future performance.

## 1. Cloning the repository
To get started, clone the repository from GitHub:
```
git clone git@github.com:apalladi/Monte-Carlo-PAC.git
```

Then, navigate into the project directory:
```
cd Monte-Carlo-PAC
```

## 2. Installing and Activating the Environment
To set up the Conda environment with all required dependencies, follow these steps:

1. Make sure you have Conda installed on your system.

2. Create the environment using the provided `environment.yml` file:
```
conda env create -f environment.yml
```

3. Once the environment is created, activate it with:
```
conda activate pac-monte-carlo
```

Now you are ready to start working with the project and run simulations!


## 3. Technical Details

The repository is structured as follows. There are 4 modules in the `src` folder.

### 3.1 Data Module

This module provides functions to retrieve and process historical stock price data from Yahoo Finance.

The module includes two primary functions:
1. `import_data`: Retrieves historical daily closing prices for a specific stock ticker.
2. `generate_df_from_list`: Generates a DataFrame of historical closing prices for multiple stock tickers.

Both functions rely on Yahoo Finance as the data source and use `pandas` for data manipulation. The data can be fetched starting from a given date up to the current date. The resulting DataFrames are indexed by date and contain only the closing price for each stock ticker.

**Functions:**
----------
- `import_data(ticker, starting_date)`: Retrieves historical closing prices for a specific stock ticker.
- `generate_df_from_list(list_tickers, starting_time)`: Retrieves and combines historical closing prices for a list of stock tickers into a single DataFrame.

**Example usage:**
--------------
```python
# Import historical data for Apple and Microsoft starting from January 1, 2020
df = generate_df_from_list(['AAPL', 'MSFT'], '2020-01-01')
print(df.head())
```

### 3.2 Simulation Module

**Investment Simulation Module**

This module provides functionality to simulate periodic investment strategies and compute summary statistics based on historical stock data. It includes functions to simulate single or multiple investments over a given time period and compute the resulting returns. Additionally, it supports running simulations across various investment durations and summarizing the outcomes.

**Functions:**
----------
- `simulate_single_investment(data, n_years, starting_point, verbose=False)`: Simulates a single periodic investment strategy over a specified number of years.
- `simulate_multiple_investments(data, n_years, n_simulations)`: Runs multiple investment simulations with different starting points and returns a list of annualized net returns.
- `simulate_multiple_durations(data, years_grid, n_simulations)`: Simulates investments for a range of durations and computes summary statistics for each duration based on multiple simulations.


### 3.3 Stats Module

**This module provides functionality to analyze investment returns.**

It includes a function to compute summary statistics from a list of investment returns, including minimum, maximum, median returns, and probabilities of non-negative returns and returns exceeding a specified threshold (e.g., inflation).

**Functions:**
----------
- `compute_summary_stats(returns_list)`: Calculates summary statistics for a list of investment returns.

### 3.4 Plot Module

**This module provides a function for visualizing investment simulation results.**

It generates plots that illustrate the median return and the probability of positive returns over various investment durations.

**Function:**
---------
- `show_results(years_grid, results, title, show_figure=True, save_figure=False)`: Plots simulation results, optionally saving the figure.

**Disclaimer:**
---------------
This repository does not contain any financial advice or recommendations of any kind. The simulations provided are based solely on historical data and do not possess predictive power for future investments. Users are encouraged to conduct their own research and consult with a financial advisor before making any investment decisions.


