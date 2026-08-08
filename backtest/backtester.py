from strategy.strategy import generate_signal
from backtest.performance import calculate_performance
from backtest.trade import Trade
from risk.risk_manager import calculate_position_size


def run_backtest(
    data,
    starting_balance=1000,
    risk_percent=1,
    stop_loss_percent=1,
    take_profit_percent=2
):
    balance = starting_balance

    position = None
    entry_price = 0
    stop_loss = 0
    take_profit = 0
    position_size = 0

    trades = []

    for i in range(30, len(data)):

        current_data = data.iloc[:i + 1]

        open_price = data["open"].iloc[i]
        high_price = data["high"].iloc[i]
        low_price = data["low"].iloc[i]
        close_price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # ==========================
        # OPEN LONG POSITION
        # ==========================

        if signal == "BUY" and position is None:

            entry_price = close_price

            stop_loss = entry_price * (
                1 - stop_loss_percent / 100
            )

            take_profit = entry_price * (
                1 + take_profit_percent / 100
            )

            position_size = calculate_position_size(
                balance,
                risk_percent,
                entry_price,
                stop_loss
            )

            position = "LONG"

        # ==========================
        # MANAGE LONG POSITION
        # ==========================

        elif position == "LONG":

            exit_price = None
            exit_reason = None

            # Stop-loss hit
            if low_price <= stop_loss:

                exit_price = stop_loss
                exit_reason = "STOP_LOSS"

            # Take-profit hit
            elif high_price >= take_profit:

                exit_price = take_profit
                exit_reason = "TAKE_PROFIT"

            # Strategy exit
            elif signal == "SELL":

                exit_price = close_price
                exit_reason = "STRATEGY_EXIT"

            # ==========================
            # CLOSE TRADE
            # ==========================

            if exit_price is not None:

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

                trade_data = trade.to_dict()

                trade_data["exit_reason"] = exit_reason

                trades.append(trade_data)

                position = None
                position_size = 0

    performance = calculate_performance(
        trades,
        starting_balance
    )

    return performance