from strategy.strategy import generate_signal
from backtest.performance import calculate_performance


def run_backtest(data, starting_balance=1000):
    balance = starting_balance
    position = None
    entry_price = 0

    trades = []

    for i in range(30, len(data)):
        current_data = data.iloc[:i + 1]
        price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # Open long position
        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price

        # Close long position
        elif signal == "SELL" and position == "LONG":
            profit = price - entry_price

            balance += profit

            trades.append({
                "entry_price": entry_price,
                "exit_price": price,
                "profit": profit
            })

            position = None

    performance = calculate_performance(
        trades,
        starting_balance
    )

    return performance