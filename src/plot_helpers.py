# src/plot_helpers.py

import matplotlib.pyplot as plt
	
def plot_ci_bar(result_dict, title="Expanding Regime Long-Short Spread", filename="expanding_regime_bar.png", order=None, ylabel="Daily Return (Decimal)"):
    """
    Plot bar chart of mean long-short return with 95% CI.

    Parameters:
        result_dict (dict): Dict with 'mean', 'ci_lower', 'ci_upper' for each regime
        title (str): Plot title
        filename (str): Output filename for PNG export
        order (list): Optional fixed order for labels
        ylabel (str): Y-axis label
    """
    labels = order if order else list(result_dict.keys())
    means = [result_dict[k]["mean"] for k in labels]
    lowers = [result_dict[k]["mean"] - result_dict[k]["ci_lower"] for k in labels]
    uppers = [result_dict[k]["ci_upper"] - result_dict[k]["mean"] for k in labels]

    fig, ax = plt.subplots()
    bars = ax.bar(labels, means, yerr=[lowers, uppers], capsize=10)
    ax.axhline(0, color='gray', linewidth=1, linestyle='--')
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.annotate(f"{mean:.4f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("../research/plots/" + filename)
    plt.show()