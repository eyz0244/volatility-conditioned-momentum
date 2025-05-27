# src/backtest_engine.py

import pandas as pd
import numpy as np
from typing import Callable

def model_decile_long_short(test_df: pd.DataFrame) -> float:
    """
    Long-short return from top and bottom decile of factor scores in test_df.

    Parameters:
        test_df (pd.DataFrame): DataFrame with 'factor' and 'returns' columns for one date.

    Returns:
        float: Average return spread between top and bottom decile.
    """
    scores = test_df["factor"]
    rets = test_df["returns"]

    # Rank factor scores to identify top and bottom deciles
    ranked = scores.rank(method="first")
    n = len(ranked)

    # Define long and short positions
    long = ranked[ranked > 0.9 * n].index
    short = ranked[ranked <= 0.1 * n].index

    # Return average long-short spread
    return rets.loc[long].mean() - rets.loc[short].mean()

def walk_forward_model_apply(
    factor: pd.DataFrame,
    returns: pd.DataFrame,
    regime: pd.Series,
    target_regime: str,
    model_fn: Callable,
    lag_days: int = 5,
    train_window: int = 0,
    test_window: int = 21,
    step: int = 21,
    min_obs: int = 20
) -> pd.DataFrame:
    """
    Generic walk-forward evaluation applying `model_fn` to each test slice,
    conditioned on a specific regime.

    Parameters:
        factor (pd.DataFrame): Factor values [index: date, columns: tickers]
        returns (pd.DataFrame): Forward returns [index: date, columns: tickers]
        regime (pd.Series): Regime labels [index: date]
        target_regime (str): Regime label to filter test dates
        model_fn (Callable): Function to compute signal (e.g., long-short return)
        lag_days (int): Delay between regime observation and model decision
        train_window (int): Number of days in training window (0 = no training)
        test_window (int): Number of days in test window per walk-forward step
        step (int): Days to move forward between walk-forward iterations
        min_obs (int): Minimum required non-NaN assets to compute signal

    Returns:
        pd.DataFrame: Long-short returns indexed by test date
    """
    # Align dates across all inputs
    all_dates = factor.index.intersection(returns.index).intersection(regime.index)
    results = []

    # Lag regime label to ensure causality
    regime_lagged = regime.shift(lag_days)

    # Print valid testable days, used for diagnostics so comment out after testing
    # print("Valid testable dates in " + target_regime + " after regime lag:", len(regime_lagged[regime_lagged == target_regime].dropna().index.intersection(factor.dropna().index).intersection(returns.dropna().index)))

    # Iterate over walk-forward windows
    for start in range(0, len(all_dates) - train_window - test_window, step):
        train_idx = all_dates[start : start + train_window] if train_window > 0 else []
        test_idx = all_dates[start + train_window : start + train_window + test_window]

        # Evaluate each test date in current slice
        for date in test_idx:
            # Skip if regime does not match target
            if regime_lagged.loc[date] != target_regime:
                results.append((date, np.nan))
                continue

            f = factor.loc[date]
            r = returns.loc[date]

            # Filter to stocks with non-missing factor and return values
            valid = f.notna() & r.notna()
            if valid.sum() < min_obs:
                results.append((date, np.nan))
                continue

            test_df = pd.DataFrame({
                "factor": f,
                "returns": r
            }).dropna()

            # Evaluate using model function
            if train_window == 0:
                ret = model_fn(test_df)
            else:
                train_df = pd.concat([
                    factor.loc[train_idx].stack().rename("factor"),
                    returns.loc[train_idx].stack().rename("returns")
                ], axis=1).dropna()
                ret = model_fn(train_df, test_df)

            results.append((date, ret))

    return pd.DataFrame(results, columns=["date", "returns"]).set_index("date")
