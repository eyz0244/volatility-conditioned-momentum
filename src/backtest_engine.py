import pandas as pd
import numpy as np
from typing import Callable

def model_decile_long_short(test_df: pd.DataFrame) -> float:
    """
    Long-short return from top and bottom decile of factor scores in test_df.
    """
    scores = test_df["factor"]
    rets = test_df["returns"]
    ranked = scores.rank()
    n = len(ranked)
    long = ranked[ranked > 0.9 * n].index
    short = ranked[ranked <= 0.1 * n].index
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
    step: int = 21
) -> pd.DataFrame:
    """
    Generic walk-forward evaluation applying `model_fn` to each test slice,
    conditioned on a specific regime.

    If train_window == 0, skips train_df construction for efficiency.

    Returns:
        pd.DataFrame with 'returns' column indexed by test date
    """
    all_dates = factor.index.intersection(returns.index).intersection(regime.index)
    results = []
    regime_lagged = regime.shift(lag_days)

    for start in range(0, len(all_dates) - train_window - test_window, step):
        train_idx = all_dates[start : start + train_window] if train_window > 0 else []
        test_idx = all_dates[start + train_window : start + train_window + test_window]

        for date in test_idx:
            if regime_lagged.loc[date] != target_regime:
                results.append((date, np.nan))
                continue

            f = factor.loc[date]
            r = returns.loc[date]
            valid = f.notna() & r.notna()
            if valid.sum() < 20:
                results.append((date, np.nan))
                continue

            test_df = pd.DataFrame({
                "factor": f,
                "returns": r
            }).dropna()

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