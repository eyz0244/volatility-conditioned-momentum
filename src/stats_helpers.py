# src/stats_helper.py

import numpy as np
import pandas as pd

def bootstrap_mean_diff(series1: pd.Series, series2: pd.Series, n_iter: int = 1000, seed: int = None) -> dict:
    """
    Compute bootstrap confidence interval and p-value for the difference in means between two series
    under the null hypothesis that both come from the same distribution.

    Parameters:
        series1 (pd.Series): First sample
        series2 (pd.Series): Second sample
        n_iter (int): Number of bootstrap iterations
        seed (int): Random seed for reproducibility

    Returns:
        dict: mean_diff, ci_lower, ci_upper, p_value
    """
    if seed is not None:
        np.random.seed(seed)

    series1 = series1.dropna().values
    series2 = series2.dropna().values
    observed_diff = series1.mean() - series2.mean()

    pooled = np.concatenate([series1, series2])
    n1 = len(series1)
    n2 = len(series2)

    boot_diffs = []
    for _ in range(n_iter):
        resample = np.random.choice(pooled, size=n1 + n2, replace=True)
        s1 = resample[:n1]
        s2 = resample[n1:]
        boot_diffs.append(s1.mean() - s2.mean())

    boot_diffs = np.array(boot_diffs)
    lower = np.percentile(boot_diffs, 2.5)
    upper = np.percentile(boot_diffs, 97.5)
    pval = (np.abs(boot_diffs) >= np.abs(observed_diff)).mean()

    
    return {
    "mean_1": series1.mean(),
    "mean_2": series2.mean(),
    "n_1": len(series1),
    "n_2": len(series2),
    "mean_diff": observed_diff,
    "bootstrap_diff": boot_diffs.mean(),	
    "ci_lower": lower,
    "ci_upper": upper,
    "p_value": pval
}
	
	

def bootstrap_ci(series: pd.Series, n_iter: int = 1000, seed: int = None) -> dict:
    """
    Compute bootstrap confidence interval for the mean of a single series.

    Parameters:
        series (pd.Series): Sample data
        n_iter (int): Number of bootstrap iterations
        seed (int): Random seed for reproducibility

    Returns:
        dict: mean, ci_lower, ci_upper
    """
    if seed is not None:
        np.random.seed(seed)

    values = series.dropna().values
    boot_means = [
        np.mean(np.random.choice(values, size=len(values), replace=True))
        for _ in range(n_iter)
    ]

    lower = np.percentile(boot_means, 2.5)
    upper = np.percentile(boot_means, 97.5)

    return {
        "mean": np.mean(values),
        "ci_lower": lower,
        "ci_upper": upper
    }