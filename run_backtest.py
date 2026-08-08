import pandas as pd

from backtest.backtester import run_backtest


data = pd.read_csv("data/sample_prices.csv")

result = run_backtest(data)


print("================================")
print("      AI TRADING BOT")
print("      BACKTEST RESULTS")
print("================================")

print(f"Starting Balance : ${result['ending_balance'] - result['profit_loss']:.2f}")
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