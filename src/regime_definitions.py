# src/regime_definitions.py

import pandas as pd
import numpy as np

def compute_market_volatility_regime(returns: pd.DataFrame, window: int = 20, high_q: float = 0.7, low_q: float = 0.3) -> pd.Series:
    """
    Compute market volatility regime using rolling std of market mean return.
	
	Parameters:
		returns (pd.DataFrame): Wide-format price data (rows = dates, columns = tickers)
		window (int): Rolling window in trading days
		high_q (float): Quantile for high volatility threshold
		low_q (float): Quantile for low volatility threshold

	Returns:
		pd.Series of volatility regime labels ('high_vol', 'low_vol', 'neutral')	
    """
    market_ret = returns.mean(axis=1)
    market_vol = market_ret.rolling(window=window, min_periods=window).std()
    assert market_vol.index.equals(returns.index) #"Index misalignment in rolling calculation"
	

    high_thresh = market_vol.quantile(high_q)
    low_thresh = market_vol.quantile(low_q)

    regime = pd.Series(index=market_vol.index, dtype="object")
    regime[market_vol >= high_thresh] = 'high_vol'
    regime[market_vol <= low_thresh] = 'low_vol'
    regime = regime.fillna('neutral')

    return regime

def compute_cross_sectional_dispersion_regime(returns: pd.DataFrame, window: int = 20, high_q: float = 0.7, low_q: float = 0.3) -> pd.Series:
    """
    Compute regime using cross-sectional std of returns each day.

	Parameters:
		returns (pd.DataFrame): Wide-format price data (rows = dates, columns = tickers)
		window (int): Rolling window in trading days
		high_q (float): Quantile for high dispersion threshold
    low_q (float): Quantile for low dispersion threshold

	Returns:
		pd.Series of dispersion regime labels ('high_disp', 'low_disp', 'neutral')	
    """
    dispersion = returns.std(axis=1).rolling(window=window, min_periods=window).mean()
    assert dispersion.index.equals(returns.index) #"Index misalignment in rolling calculation"
	

    high_thresh = dispersion.quantile(high_q)
    low_thresh = dispersion.quantile(low_q)

    regime = pd.Series(index=dispersion.index, dtype="object")
    regime[dispersion >= high_thresh] = 'high_disp'
    regime[dispersion <= low_thresh] = 'low_disp'
    regime = regime.fillna('neutral')

    return regime