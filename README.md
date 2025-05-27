# Volatility-Conditioned Factor Performance

This project analyzes how equity factor returns—specifically momentum and reversal—vary across market volatility and dispersion regimes.  
We test whether momentum signals exhibit greater stability in low-volatility and low-dispersion environments.

## Repository Structure

- `notebooks/`: step-by-step development, from universe construction to robustness testing  
- `src/`: reusable Python modules (e.g., factor construction, regime definitions, backtesting)  
- `research/`: visualizations and formal write-up  
- `data/`: raw and processed data (excluded via `.gitignore`)  

## Methods

- Momentum and reversal factor engineering  
- Regime definition using rolling market volatility and cross-sectional dispersion  
- Conditional decile backtests across volatility and dispersion states  
- Walk-forward validation with lagged regime detection  
- Bootstrap inference to assess statistical robustness  

## Status

Active. Full cleaned code and final LaTeX write-up (`Zhao_MomentumRegimes_2025_v1.pdf`) are included under `research/`.