# Algorithmic Trading Strategy - Round 1 Task

## Overview
This project implements a complete algorithmic trading strategy using:
- Python 3
- Backtrader
- yfinance
- Walk-Forward Analysis
- Robustness Scoring

## Strategy
The strategy combines:
1. Fast EMA / Slow EMA crossover
2. RSI confirmation
3. ATR-based stop loss
4. Risk-based position sizing

## Project Structure
```
algo_trading_round1/
│
├── main.py
├── strategy.py
├── walk_forward.py
├── robustness.py
├── metrics.py
├── requirements.txt
└── README.md
```

## Installation
```bash
pip install -r requirements.txt
```

## Run Backtest
```bash
python main.py
```

## Run Walk Forward Analysis
```bash
python walk_forward.py
```

## Metrics To Report
After execution, report:
- Percentage Return on Capital
- Maximum Drawdown
- Walk-Forward Analysis Score
- Robustness Score

## Suggested Submission Format

| Metric | Value |
|---|---|
| Stock Symbol | AAPL |
| Starting Capital | $100000 |
| Percentage Return on Capital | XX.X% |
| Maximum Drawdown | XX.X% |
| Walk-Forward Analysis Score | XX |
| Robustness Score | XX |

## Notes
- Uses 5+ years of daily data from Yahoo Finance.
- Designed to avoid overfitting.
- Includes walk-forward validation and robustness scoring.