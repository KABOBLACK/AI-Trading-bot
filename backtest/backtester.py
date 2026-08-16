from strategy.strategy import generate_signal
from backtest.performance import calculate_performance
from backtest.trade import Trade
from backtest.trade_logger import save_trades
from risk.risk_manager import calculate_position_size
import math


def run_backtest(
    data,
    starting_balance=1000,
    risk_percent=1,
    stop_loss_percent=1,
    take_profit_percent=2,
    fee_percent=0.1,
    slippage_percent=0.05
):
    balance = float(starting_balance)

    position = None
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    position_size = 0.0

    trades = []

    # Start at index 30 because strategy uses a 30-period long MA
    for i in range(30, len(data)):

        current_data = data.iloc[: i + 1]

        high_price = float(data["high"].iloc[i])
        low_price = float(data["low"].iloc[i])
        close_price = float(data["close"].iloc[i])

        signal = generate_signal(current_data)

        # Open LONG position
        if signal == "BUY" and position is None:

            entry_price = close_price * (1 + slippage_percent / 100.0)

            stop_loss = entry_price * (1 - stop_loss_percent / 100.0)

            take_profit = entry_price * (1 + take_profit_percent / 100.0)

            # calculate_position_size should return number of units (float/int) or 0
            position_size = calculate_position_size(
                balance,
                risk_percent,
                entry_price,
                stop_loss
            )

            # Defensive checks: ensure numeric, non-negative, and affordable
            try:
                position_size = float(position_size)
            except Exception:
                position_size = 0.0

            position_size = max(0.0, position_size)

            # Cap to what the balance can actually buy (in whole units)
            max_affordable = math.floor(balance / entry_price) if entry_price > 0 else 0
            if max_affordable <= 0 or position_size < 1e-9:
                # cannot open a position
                position = None
                position_size = 0.0
            else:
                # If position_size is fractional and you need integer units, floor it
                if not position_size.is_integer():
                    # keep fractional if intended; otherwise floor to integer units
                    position_size = math.floor(position_size)
                    if position_size <= 0:
                        position = None
                        continue

                # Cap by affordability
                position_size = min(position_size, max_affordable)
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

                actual_exit_price = exit_price * (1 - slippage_percent / 100.0)

                gross_profit = (actual_exit_price - entry_price) * position_size

                entry_value = entry_price * position_size

                exit_value = actual_exit_price * position_size

                fees = (entry_value * fee_percent / 100.0) + (exit_value * fee_percent / 100.0)

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
                trade_data["fees"] = round(fees, 8)

                trades.append(trade_data)

                position = None
                position_size = 0.0

    # If there's an open position at the end of the data, close it at last close
    if position == "LONG":
        last_close = float(data["close"].iloc[-1])
        actual_exit_price = last_close * (1 - slippage_percent / 100.0)
        gross_profit = (actual_exit_price - entry_price) * position_size
        entry_value = entry_price * position_size
        exit_value = actual_exit_price * position_size
        fees = (entry_value * fee_percent / 100.0) + (exit_value * fee_percent / 100.0)
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
        trade_data["exit_reason"] = "END_OF_DATA"
        trade_data["fees"] = round(fees, 8)
        trades.append(trade_data)

    # Save trade history
    save_trades(trades)

    # Calculate performance
    performance = calculate_performance(trades, starting_balance)

    return performance
