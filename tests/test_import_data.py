import pandas as pd
from datetime import datetime, timedelta
from src.data import *

def test_import_data():
    # Import data for S&P 500 (^GSPC) starting from 2020-01-01
    df = import_data('^GSPC', starting_date='2020-01-01')
    
    # Calculate the number of days between today and the starting date
    delta = datetime.now() - datetime(2020, 1, 1)
    days_difference = delta.days
    
    # Estimate the number of trading days assuming ~252 trading days per year
    trading_days_per_year = 252
    estimated_length = days_difference / 365 * trading_days_per_year
    
    # Assert that the imported data is a Pandas DataFrame
    assert isinstance(df, pd.DataFrame), "The time series must be a Pandas DataFrame"
    
    # Assert that the length of the DataFrame is within a reasonable range
    assert abs(len(df) - estimated_length) <= 30, \
        "The length of the time series is outside the expected range."
    
def test_import_multiple_data():
    # Import data for MSCI World and EU Bond starting from 2020-01-01
    df = generate_df_from_list(['SWDA.MI', 'XGLE.MI'], starting_date='2020-01-01')
    
    # Calculate the number of days between today and the starting date
    delta = datetime.now() - datetime(2020, 1, 1)
    days_difference = delta.days
    
    # Estimate the number of trading days assuming ~252 trading days per year
    trading_days_per_year = 252
    estimated_length = (days_difference / 365) * trading_days_per_year
    
    # Assert that the imported data is a Pandas DataFrame
    assert isinstance(df, pd.DataFrame), "The time series must be a Pandas DataFrame"
    
    # Assert that the length of the DataFrame is within a reasonable range
    assert abs(len(df) - estimated_length) <= 30, \
        "The length of the time series is outside the expected range."
    
    # Assert that the DataFrame has 2 columns
    assert df.shape[1] == 2, "The DataFrame must have 2 columns"
    
    # Optionally, check that the DataFrame has expected column names
    expected_columns = ['SWDA.MI', 'XGLE.MI']
    assert list(df.columns) == expected_columns, f"Expected columns are {expected_columns}, but got {df.columns.tolist()}"
    
    # Optionally, check that there are no missing values
    assert df.isnull().sum().sum() == 0, "The DataFrame should not contain missing values"


if __name__ == "__main__":
    test_import_data()
    test_import_multiple_data()