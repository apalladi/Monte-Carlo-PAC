import pandas as pd
import numpy as np
from src.data import import_data
from src.simulations import simulate_single_investment
from math import isclose

def test_single_investment():

    interest = 5
    tax = 26
    df = pd.DataFrame(np.linspace(100, 100+interest*4, 1008), columns=['close'])    
    
    final_return = simulate_single_investment(df, n_years=2, starting_point=5, verbose=False)

    isclose(final_return, interest*(1-tax/100), abs_tol=10**-1)