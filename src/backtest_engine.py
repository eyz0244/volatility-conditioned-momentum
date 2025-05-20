import pandas as pd
import numpy as np

def compute_long_short_returns(factor: pd.DataFrame, returns: pd.DataFrame, regime: pd.Series, target_regime: str) -> pd.Series:
    """
    Compute long-short returns of a factor under a specific regime.

    Parameters:
        factor (DataFrame): Daily factor scores [index: date, columns: tickers]

    Returns:
        pd.Series of returns
	
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

        long = ranked[ranked > 0.9 * n].index # Long: strictly top 10% (to avoid oversampling ties)
        short = ranked[ranked <= 0.1 * n].index # Short: inclusive bottom 10% (to capture all weak signals including ties)

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
    test_window: int = 21,
	step=5
) -> pd.Series:
    """
    Perform walk-forward evaluation of long-short factor returns, conditioned on a specific volatility / dispersion regime.

    For each rolling train/test split:
    - Regime is lagged by `lag_days` to reflect signal availability delay.
    - On test days where lagged regime matches `target_regime`, compute long-short return:
      top decile minus bottom decile based on cross-sectional factor ranking.

    Parameters:
        factor (DataFrame): Daily factor scores [index: date, columns: tickers]
        returns (DataFrame): Daily forward returns [same shape as factor]
        regime (Series): Daily regime label (e.g., 'low', 'high') [index: date]
        target_regime (str): Regime to filter on during test
        lag_days (int): Lag applied to regime before test filtering
        train_window (int): Lookback window for regime conditioning (retained for flexibility)
        test_window (int): Test window length
		step: Number of days to shift forward between each walk-forward iteration.
			Smaller values (e.g. 1 or 5) produce overlapping train/test windows and smoother evaluation curves.
			Larger values (e.g. equal to test_window) produce non-overlapping evaluations.

    Returns:
        Returns: DataFrame: Daily long-short returns [index: date, column: 'returns'] for the specified regime	
    """
    all_dates = factor.index.intersection(returns.index).intersection(regime.index)
    results = []

    for start in range(0, len(all_dates) - train_window - test_window, step):
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
			
