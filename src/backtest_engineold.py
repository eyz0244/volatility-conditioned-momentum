import pandas as pd
import numpy as np

def compute_long_short_returns(factor: pd.DataFrame, returns: pd.DataFrame, regime: pd.Series, target_regime: str) -> pd.Series:
    """
    Compute long-short returns of a factor under a specific regime.
    """
    daily_ls_ret = []

    for date in factor.index.intersection(regime.index):
        if regime.loc[date] != target_regime:
            daily_ls_ret.append(np.nan)
            continue

        scores = factor.loc[date]
        rets = returns.loc[date]
        valid = scores.notna() & rets.notna()

        if valid.sum() < 20:  # skip illiquid days
            daily_ls_ret.append(np.nan)
            continue

        ranked = scores[valid].rank()
        n = len(ranked)

        long = ranked[ranked > 0.9 * n].index
        short = ranked[ranked <= 0.1 * n].index

        ls_ret = rets[long].mean() - rets[short].mean()
        daily_ls_ret.append(ls_ret)

    return pd.Series(daily_ls_ret, index=factor.index)


def walk_forward_ls_by_regime(
    factor: pd.DataFrame,
    returns: pd.DataFrame,
    regime: pd.Series,
    target_regime: str,
    lag_days: int = 5,
    train_window: int = 252,
    test_window: int = 21
) -> pd.Series:
    """
    Walk-forward long-short returns conditioned on regime.
    """
    all_dates = factor.index.intersection(returns.index).intersection(regime.index)
    results = []

    for start in range(0, len(all_dates) - train_window - test_window, test_window):
        train_idx = all_dates[start : start + train_window]
        test_idx = all_dates[start + train_window : start + train_window + test_window]

        # regime lag
        regime_lagged = regime.shift(lag_days)

        for date in test_idx:
            if regime_lagged.loc[date] != target_regime:
                results.append((date, np.nan))
                continue

            scores = factor.loc[date]
            rets = returns.loc[date]
            valid = scores.notna() & rets.notna()
            if valid.sum() < 20:
                results.append((date, np.nan))
                continue

            ranked = scores[valid].rank()
            n = len(ranked)
            long = ranked[ranked > 0.9 * n].index
            short = ranked[ranked <= 0.1 * n].index

            ls_ret = rets[long].mean() - rets[short].mean()
            results.append((date, ls_ret))
            
    return pd.DataFrame(results, columns=['date', 'returns']).set_index('date')
			
    #return pd.Series({d: r for d, r in results})
