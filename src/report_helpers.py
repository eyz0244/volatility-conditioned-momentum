# src/report_helpers.py

def format_diff_result(diff_key: str, result: dict) -> None:
    """
    Print formatted, research-grade summary of bootstrap mean difference results.

    Parameters:
        diff_key (str): Label identifying the comparison (e.g., regime type or test method)
        result (dict): Output from bootstrap_mean_diff, must include keys:
            'mean_1', 'mean_2', 'n_1', 'n_2', 'mean_diff', 'ci_lower', 'ci_upper', 'p_value'

    Returns:
        None. Prints formatted summary directly.
    """
    # Print comparison label
    print(f"Comparison: {diff_key}")

    # Print group 1 summary (typically low volatility regime)
    print(f"Group 1 (Low Vol) — Mean: {result['mean_1']:.6f}, N: {result['n_1']}")

    # Print group 2 summary (typically high volatility regime)
    print(f"Group 2 (High Vol) — Mean: {result['mean_2']:.6f}, N: {result['n_2']}")

    # Print the observed mean difference
    print(f"Mean Difference: {result['mean_diff']:.6f}")

    # Print the bootstrap mean difference
    print(f"Boostrap Difference: {result['bootstrap_diff']:.6f}")

    # Print the 95% bootstrap confidence interval
    print(f"95% CI for Difference: [{result['ci_lower']:.6f}, {result['ci_upper']:.6f}]")

    # Print the two-sided p-value
    print(f"P-value: {result['p_value']:.3f}")

    # Print a separator line for readability
    print("-" * 50)


def format_ci_result(label: str, result: dict) -> None:
    """
    Print formatted, research-grade summary of a bootstrap CI estimate for a single return series.

    Parameters:
        label (str): Label identifying the series (e.g., 'low_vol', 'high_vol')
        result (dict): Output from bootstrap_ci, must include keys:
            'mean', 'ci_lower', 'ci_upper'

    Returns:
        None. Prints formatted summary directly.
    """
    # Print label for the series
    print(f"Regime: {label}")

    # Print the sample mean
    print(f"Mean: {result['mean']:.6f}")

    # Print the 95% bootstrap confidence interval
    print(f"95% CI: [{result['ci_lower']:.6f}, {result['ci_upper']:.6f}]")

    # Print a separator line for readability
    print("-" * 50)
