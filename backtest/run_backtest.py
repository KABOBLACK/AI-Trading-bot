from data.csv_provider import CSVDataProvider
from backtest.backtester import run_backtest


provider = CSVDataProvider(
    "data/sample_ohlcv.csv"
)

data = provider.get_ohlcv(
    symbol="BTCUSDT",
    timeframe="1h",
    limit=100
)

result = run_backtest(
    data,
    starting_balance=1000,
    risk_percent=1,
    stop_loss_percent=1,
    take_profit_percent=2
)


print("================================")
print("       AI TRADING BOT")
print("       BACKTEST RESULTS")
print("================================")

print("Symbol           : BTCUSDT")
print("Timeframe        : 1h")

print("--------------------------------")

print(f"Starting Balance : $1000.00")
print(f"Ending Balance   : ${result['ending_balance']:.2f}")
print(f"Profit / Loss    : ${result['profit_loss']:.2f}")

print("--------------------------------")

print(f"Total Trades     : {result['total_trades']}")
print(f"Winning Trades   : {result['winning_trades']}")
print(f"Losing Trades    : {result['losing_trades']}")
print(f"Win Rate         : {result['win_rate']:.2f}%")

print("--------------------------------")

print(f"Max Drawdown     : ${result['max_drawdown']:.2f}")

print("================================")