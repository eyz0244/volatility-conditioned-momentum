import numpy as np
import pandas as pd

def bootstrap_mean_diff(series1: pd.Series, series2: pd.Series, n_iter: int = 1000) -> dict:
    """
    Bootstrap the difference in means between two series.
    """
    series1 = series1.dropna().values
    series2 = series2.dropna().values

    boot_diffs = []
    for _ in range(n_iter):
        s1 = np.random.choice(series1, size=len(series1), replace=True)
        s2 = np.random.choice(series2, size=len(series2), replace=True)
        boot_diffs.append(s1.mean() - s2.mean())

    boot_diffs = np.array(boot_diffs)
    lower = np.percentile(boot_diffs, 2.5)
    upper = np.percentile(boot_diffs, 97.5)
    pval = (np.abs(boot_diffs) >= np.abs(np.mean(series1) - np.mean(series2))).mean()

    return {
        "mean_diff": np.mean(series1) - np.mean(series2),
        "ci_lower": lower,
        "ci_upper": upper,
        "p_value": pval
    }

def bootstrap_ci(series: pd.Series, n_iter: int = 1000) -> dict:
    """
    Bootstrap confidence interval for mean of a single series.
    """
    values = series.dropna().values
    boot_means = [np.mean(np.random.choice(values, size=len(values), replace=True)) for _ in range(n_iter)]

    lower = np.percentile(boot_means, 2.5)
    upper = np.percentile(boot_means, 97.5)
    return {
        "mean": np.mean(values),
        "ci_lower": lower,
        "ci_upper": upper
    }