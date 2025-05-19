import pandas as pd
import numpy as np

def compute_market_volatility_regime(price_df: pd.DataFrame, window: int = 20, high_q: float = 0.7, low_q: float = 0.3) -> pd.Series:
    """
    Compute market volatility regime using rolling std of market mean return.
    """
    returns = np.log(price_df / price_df.shift(1))
    market_ret = returns.mean(axis=1)
    market_vol = market_ret.rolling(window=window).std()

    high_thresh = market_vol.quantile(high_q)
    low_thresh = market_vol.quantile(low_q)

    regime = pd.Series(index=market_vol.index, dtype="object")
    regime[market_vol >= high_thresh] = 'high_vol'
    regime[market_vol <= low_thresh] = 'low_vol'
    regime = regime.fillna('neutral')

    return regime

def compute_cross_sectional_dispersion_regime(price_df: pd.DataFrame, window: int = 20, high_q: float = 0.7, low_q: float = 0.3) -> pd.Series:
    """
    Compute regime using cross-sectional std of returns each day.
    """
    returns = np.log(price_df / price_df.shift(1))
    dispersion = returns.std(axis=1).rolling(window=window).mean()

    high_thresh = dispersion.quantile(high_q)
    low_thresh = dispersion.quantile(low_q)

    regime = pd.Series(index=dispersion.index, dtype="object")
    regime[dispersion >= high_thresh] = 'high_disp'
    regime[dispersion <= low_thresh] = 'low_disp'
    regime = regime.fillna('neutral')

    return regime