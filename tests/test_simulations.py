from src.data import import_data
from src.simulations import simulate_single_investment
from math import isclose

def test_single_investment():

    df = import_data('^SP500TR', starting_date='2000-01-01')
    df = df.loc[df.index <='2003-12-31']
    
    assert len(df) == 1004, "Check the length of the DataFrame"
    
    final_return = simulate_single_investment(df, n_years=2, starting_point=5, verbose=False)
    
    assert isclose(final_return, -11.24, abs_tol=10**-2)