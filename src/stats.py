"""
This module provides functionality to analyze investment returns.

It includes a function to compute summary statistics from a list of investment returns,
including minimum, maximum, median returns, and probabilities of non-negative returns
and returns exceeding a specified threshold (e.g., inflation).

Functions:
----------
compute_summary_stats(returns_list):
    Calculates summary statistics for a list of investment returns.
"""

import numpy as np

def compute_summary_stats(returns_list):
    """
    Calculates summary statistics from a list of investment returns.

    This function computes key summary statistics for a given list of returns, including
    the minimum, maximum, and median return. It also calculates the probability that a
    return is non-negative (greater than 0) and the probability that a return exceeds
    2%, which can represent a threshold for inflation or a target return.

    Parameters:
    -----------
    returns_list : list or numpy.ndarray
        A list or array containing the returns to be analyzed, expressed as percentages.

    Returns:
    --------
    tuple
        A tuple containing the following summary statistics:
        - min_return (float): The minimum return in the list.
        - max_return (float): The maximum return in the list.
        - median_return (float): The median return in the list.
        - prob_non_negative (float): The probability that a return is non-negative (greater than 0).
        - prob_greater_than_inflation (float): The probability that a return is greater than 2%.
    """
    min_return = np.min(returns_list)
    max_return = np.max(returns_list)
    median_return = np.median(returns_list)
    prob_non_negative = np.mean(np.array(returns_list) > 0)
    prob_greater_than_inflation = np.mean(np.array(returns_list) > 2)

    return (
        min_return,
        max_return,
        median_return,
        prob_non_negative,
        prob_greater_than_inflation,
    )
