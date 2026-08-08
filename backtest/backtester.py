from strategy.strategy import generate_signal
from backtest.performance import calculate_performance
from backtest.trade import Trade


def run_backtest(data, starting_balance=1000):
    balance = starting_balance
    position = None
    entry_price = 0
    position_size = 1

    trades = []

    for i in range(30, len(data)):
        current_data = data.iloc[:i + 1]
        price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # Open trade
        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price

        # Close trade
        elif signal == "SELL" and position == "LONG":

            exit_price = price

            profit = (
                exit_price - entry_price
            ) * position_size

            balance += profit

            trade = Trade(
                direction="LONG",
                entry_price=entry_price,
                exit_price=exit_price,
                position_size=position_size,
                profit=profit
            )

            trades.append(trade.to_dict())

            position = None

    performance = calculate_performance(
        trades,
        starting_balance
    )

    return performance