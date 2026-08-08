import pandas as pd
from strategy.strategy import generate_signal


def run_backtest(data, starting_balance=1000):
    balance = starting_balance
    position = None
    entry_price = 0

    for i in range(30, len(data)):
        current_data = data.iloc[:i + 1]
        price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # Open position
        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price

        # Close position
        elif signal == "SELL" and position == "LONG":
            profit = price - entry_price
            balance += profit
            position = None

    return {
        "starting_balance": starting_balance,
        "ending_balance": balance,
        "profit": balance - starting_balance
    }