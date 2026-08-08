from backtest.performance import calculate_performance


def test_performance():

    trades = [
        {"profit": 20},
        {"profit": -10},
        {"profit": 30}
    ]

    result = calculate_performance(
        trades,
        starting_balance=1000
    )

    assert result["total_trades"] == 3
    assert result["winning_trades"] == 2
    assert result["losing_trades"] == 1
    assert result["profit_loss"] == 40
    assert result["ending_balance"] == 1040