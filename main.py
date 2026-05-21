import backtrader as bt
import yfinance as yf

from strategy import EMARSIATRStrategy
from metrics import calculate_return

SYMBOL = "AAPL"
STARTING_CAPITAL = 100000

# Download data
data = yf.download(
    SYMBOL,
    start="2018-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Fix MultiIndex issue from yfinance
if hasattr(data.columns, "levels"):
    data.columns = data.columns.get_level_values(0)

# Convert columns to lowercase
data.columns = [str(col).lower() for col in data.columns]

print(data.head())
print(data.columns)

# Backtrader feed
datafeed = bt.feeds.PandasData(dataname=data)

# Cerebro engine
cerebro = bt.Cerebro()

# Add strategy
cerebro.addstrategy(EMARSIATRStrategy)

# Add data
cerebro.adddata(datafeed)

# Broker settings
cerebro.broker.setcash(STARTING_CAPITAL)
cerebro.broker.setcommission(commission=0.001)

# Analyzers
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

# Run strategy
results = cerebro.run()

strat = results[0]

# Final portfolio value
final_value = cerebro.broker.getvalue()

# Calculate metrics
pct_return = calculate_return(
    STARTING_CAPITAL,
    final_value
)

max_drawdown = strat.analyzers.drawdown.get_analysis().max.drawdown

# Print results
print("\n===== RESULTS =====")
print(f"Starting Capital: ${STARTING_CAPITAL}")
print(f"Final Portfolio Value: ${final_value:.2f}")
print(f"Percentage Return on Capital: {pct_return:.2f}%")
print(f"Maximum Drawdown: {max_drawdown:.2f}%")

# Plot
cerebro.plot()
