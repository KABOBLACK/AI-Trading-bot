from strategy.strategy import generate_signal
from backtest.performance import calculate_performance
from backtest.trade import Trade
from backtest.trade_logger import save_trades
from risk.risk_manager import calculate_position_size


def run_backtest(
    data,
    starting_balance=1000,
    risk_percent=1,
    stop_loss_percent=1,
    take_profit_percent=2,
    fee_percent=0.1,
    slippage_percent=0.05
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

        high_price = data["high"].iloc[i]
        low_price = data["low"].iloc[i]
        close_price = data["close"].iloc[i]

        signal = generate_signal(current_data)

        # Open LONG position
        if signal == "BUY" and position is None:

            entry_price = close_price * (
                1 + slippage_percent / 100
            )

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

        # Manage LONG position
        elif position == "LONG":

            exit_price = None
            exit_reason = None

            if low_price <= stop_loss:

                exit_price = stop_loss
                exit_reason = "STOP_LOSS"

            elif high_price >= take_profit:

                exit_price = take_profit
                exit_reason = "TAKE_PROFIT"

            elif signal == "SELL":

                exit_price = close_price
                exit_reason = "STRATEGY_EXIT"

            if exit_price is not None:

                actual_exit_price = exit_price * (
                    1 - slippage_percent / 100
                )

                gross_profit = (
                    actual_exit_price - entry_price
                ) * position_size

                entry_value = (
                    entry_price * position_size
                )

                exit_value = (
                    actual_exit_price * position_size
                )

                fees = (
                    entry_value * fee_percent / 100
                    + exit_value * fee_percent / 100
                )

                net_profit = gross_profit - fees

                balance += net_profit

                trade = Trade(
                    direction="LONG",
                    entry_price=entry_price,
                    exit_price=actual_exit_price,
                    position_size=position_size,
                    profit=net_profit
                )

                trade_data = trade.to_dict()

                trade_data["exit_reason"] = exit_reason
                trade_data["fees"] = fees

                trades.append(trade_data)

                position = None
                position_size = 0

    # Save trade history
    save_trades(trades)

    # Calculate performance
    performance = calculate_performance(
        trades,
        starting_balance
    )

    return performance