
# src/regime_definitions.py

import pandas as pd
import numpy as np

def compute_market_volatility_regime(
    returns: pd.DataFrame,
    window: int = 20,
    high_q: float = 0.7,
    low_q: float = 0.3,
    quantile_window: int = 252,
    quantile_method: str = "rolling"  # Options: "rolling", "expanding", "static"
) -> pd.Series:
    market_ret = returns.mean(axis=1)
    market_vol = market_ret.rolling(window=window, min_periods=window).std()
    assert market_vol.index.equals(returns.index)

    if quantile_method == "rolling":
        high_thresh = market_vol.rolling(quantile_window, min_periods=window).apply(
            lambda x: np.quantile(x, high_q), raw=True
        )
        low_thresh = market_vol.rolling(quantile_window, min_periods=window).apply(
            lambda x: np.quantile(x, low_q), raw=True
        )
    elif quantile_method == "expanding":
        high_thresh = pd.Series(index=market_vol.index, dtype=float)
        low_thresh = pd.Series(index=market_vol.index, dtype=float)
        for i, t in enumerate(market_vol.index):
            subset = market_vol.iloc[:i+1].dropna()
            if len(subset) >= window:
                high_thresh[t] = np.quantile(subset, high_q)
                low_thresh[t] = np.quantile(subset, low_q)
    elif quantile_method == "static":
        high_val = np.quantile(market_vol.dropna(), high_q)
        low_val = np.quantile(market_vol.dropna(), low_q)
        high_thresh = pd.Series(high_val, index=market_vol.index)
        low_thresh = pd.Series(low_val, index=market_vol.index)
    else:
        raise ValueError("quantile_method must be one of: 'rolling', 'expanding', 'static'")

    regime = pd.Series("neutral", index=market_vol.index)
    regime[market_vol >= high_thresh] = "high_vol"
    regime[market_vol <= low_thresh] = "low_vol"

    return regime


def compute_cross_sectional_dispersion_regime(
    returns: pd.DataFrame,
    window: int = 20,
    high_q: float = 0.7,
    low_q: float = 0.3,
    quantile_window: int = 252,
    quantile_method: str = "rolling"  # Options: "rolling", "expanding", "static"
) -> pd.Series:
    dispersion = returns.std(axis=1).rolling(window=window, min_periods=window).mean()
    assert dispersion.index.equals(returns.index)

    if quantile_method == "rolling":
        high_thresh = dispersion.rolling(quantile_window, min_periods=window).apply(
            lambda x: np.quantile(x, high_q), raw=True
        )
        low_thresh = dispersion.rolling(quantile_window, min_periods=window).apply(
            lambda x: np.quantile(x, low_q), raw=True
        )
    elif quantile_method == "expanding":
        high_thresh = pd.Series(index=dispersion.index, dtype=float)
        low_thresh = pd.Series(index=dispersion.index, dtype=float)
        for i, t in enumerate(dispersion.index):
            subset = dispersion.iloc[:i+1].dropna()
            if len(subset) >= window:
                high_thresh[t] = np.quantile(subset, high_q)
                low_thresh[t] = np.quantile(subset, low_q)
    elif quantile_method == "static":
        high_val = np.quantile(dispersion.dropna(), high_q)
        low_val = np.quantile(dispersion.dropna(), low_q)
        high_thresh = pd.Series(high_val, index=dispersion.index)
        low_thresh = pd.Series(low_val, index=dispersion.index)
    else:
        raise ValueError("quantile_method must be one of: 'rolling', 'expanding', 'static'")

    regime = pd.Series("neutral", index=dispersion.index)
    regime[dispersion >= high_thresh] = "high_disp"
    regime[dispersion <= low_thresh] = "low_disp"

    return regime
