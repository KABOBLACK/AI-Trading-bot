def calculate_performance(trades, starting_balance):
    """
    Calculate basic trading performance statistics.
    """

    if not trades:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "profit_loss": 0,
            "ending_balance": starting_balance,
            "max_drawdown": 0
        }

    profits = [trade["profit"] for trade in trades]

    winning_trades = sum(1 for profit in profits if profit > 0)
    losing_trades = sum(1 for profit in profits if profit < 0)

    total_trades = len(profits)

    win_rate = (winning_trades / total_trades) * 100

    profit_loss = sum(profits)

    ending_balance = starting_balance + profit_loss

    # Calculate maximum drawdown
    balance = starting_balance
    peak = starting_balance
    max_drawdown = 0

    for profit in profits:
        balance += profit

        if balance > peak:
            peak = balance

        drawdown = peak - balance

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 2),
        "profit_loss": round(profit_loss, 2),
        "ending_balance": round(ending_balance, 2),
        "max_drawdown": round(max_drawdown, 2)
    }