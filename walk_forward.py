import pandas as pd
import yfinance as yf
import backtrader as bt

from strategy import EMARSIATRStrategy
from metrics import calculate_return, calculate_wfa_efficiency

SYMBOL = "AAPL"
STARTING_CAPITAL = 100000

# Download data
data = yf.download(
    SYMBOL,
    start="2015-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Fix MultiIndex issue
if hasattr(data.columns, "levels"):
    data.columns = data.columns.get_level_values(0)

# Convert to lowercase
data.columns = [str(col).lower() for col in data.columns]

data = data.dropna()

# Walk-forward windows
windows = [
    ("2015-01-01", "2018-01-01", "2018-01-02", "2019-01-01"),
    ("2016-01-01", "2019-01-01", "2019-01-02", "2020-01-01"),
    ("2017-01-01", "2020-01-01", "2020-01-02", "2021-01-01"),
]

scores = []

for train_start, train_end, test_start, test_end in windows:

    print(f"\nTraining: {train_start} -> {train_end}")
    print(f"Testing : {test_start} -> {test_end}")

    train = data.loc[train_start:train_end]
    test = data.loc[test_start:test_end]

    # Train data feed
    train_feed = bt.feeds.PandasData(dataname=train)

    # Test data feed
    test_feed = bt.feeds.PandasData(dataname=test)

    # Train backtest
    cerebro_train = bt.Cerebro()
    cerebro_train.addstrategy(EMARSIATRStrategy)
    cerebro_train.adddata(train_feed)
    cerebro_train.broker.setcash(STARTING_CAPITAL)

    cerebro_train.run()

    train_final = cerebro_train.broker.getvalue()

    train_return = calculate_return(
        STARTING_CAPITAL,
        train_final
    )

    
    cerebro_test = bt.Cerebro()
    cerebro_test.addstrategy(EMARSIATRStrategy)
    cerebro_test.adddata(test_feed)
    cerebro_test.broker.setcash(STARTING_CAPITAL)

    cerebro_test.run()

    test_final = cerebro_test.broker.getvalue()

    test_return = calculate_return(
        STARTING_CAPITAL,
        test_final
    )

    # WFA efficiency
    efficiency = calculate_wfa_efficiency(
        train_return,
        test_return
    )

    scores.append(efficiency)

    print(f"In-Sample Return : {train_return:.2f}%")
    print(f"Out-Sample Return: {test_return:.2f}%")
    print(f"Efficiency Score : {efficiency:.2f}")

average_score = sum(scores) / len(scores)

print("\n===== WALK FORWARD ANALYSIS =====")
print(f"Average Walk Forward Efficiency: {average_score:.2f}")