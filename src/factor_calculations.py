# src/factor_calculations.py

import pandas as pd
import numpy as np

def compute_log_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log returns from adjusted prices.
	
    Parameters:
        price_df (pd.DataFrame): Wide-format price data (rows = dates, columns = tickers)
    """
    return np.log(price_df / price_df.shift(1))

def compute_momentum(price_df: pd.DataFrame, lag: int = 21, lookback: int = 252) -> pd.DataFrame:
    """
    Compute momentum: (P_{t-lag} / P_{t-lookback}) - 1
    Default: lag=21 days, lookback=252 days (~1 year)

    Parameters:
        price_df (pd.DataFrame): Wide-format price data (rows = dates, columns = tickers)
    """
    return price_df.shift(lag) / price_df.shift(lookback) - 1

def compute_reversal(returns_df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Compute short-term reversal: rolling sum of past N returns.

    Parameters:
        returns_df (pd.DataFrame): Wide-format returns data (rows = dates, columns = tickers)
    """
    return returns_df.rolling(window=window).sum()

def compute_volatility(returns_df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Compute rolling volatility (standard deviation of returns).

    Parameters:
        returns_df (pd.DataFrame): Wide-format returns data (rows = dates, columns = tickers)
    """
    return returns_df.rolling(window = window).std()