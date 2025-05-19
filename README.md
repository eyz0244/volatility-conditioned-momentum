# Volatility-Conditioned Factor Performance

This research project investigates how equity factor returns vary across different market volatility regimes.  
We test the hypothesis that momentum signals perform more consistently during low-volatility periods.

## Structure

- `notebooks/`: step-by-step development, from universe construction to robustness tests
- `src/`: reusable Python modules (e.g., factor construction, backtest engine)
- `research/`: visualizations and write-up
- `data/`: raw and processed data (excluded from version control)

## Methods

- Momentum and reversal factor construction
- Regime definition using rolling market volatility
- Conditional decile backtests
- Walk-forward validation with regime lags
- Bootstrap-based robustness testing

## Status

Work in progress. Final cleaned code and full write-up (LaTeX + PDF) will be released in upcoming versions.