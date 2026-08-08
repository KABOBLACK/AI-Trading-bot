from strategy.strategy import generate_signal
from backtest.performance import calculate_performance
from backtest.trade import Trade
from risk.risk_manager import calculate_position_size


def run_backtest(
    data,
    starting_balance=1000,
    risk_percent=1
):
    balance = starting_balance
    position = None

    entry_price = 0
    stop_loss = 0
    position_size = 0

    trades = []

    for i in range(30, len(data)):
        current_data = data.iloc[:i + 1]
        price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # Open LONG position
        if signal == "BUY" and position is None:

            entry_price = price

            # Example: 1% stop-loss
            stop_loss = entry_price * 0.99

            position_size = calculate_position_size(
                balance,
                risk_percent,
                entry_price,
                stop_loss
            )

            position = "LONG"

        # Close LONG position
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
            position_size = 0

    performance = calculate_performance(
        trades,
        starting_balance
    )

    return performance