import pandas as pd

from backtest.backtester import run_backtest


data = pd.read_csv("data/sample_prices.csv")

result = run_backtest(data)

print("BACKTEST RESULTS")
print("----------------")
print(f"Starting balance: ${result['starting_balance']:.2f}")
print(f"Ending balance:   ${result['ending_balance']:.2f}")
print(f"Profit/Loss:      ${result['profit']:.2f}")