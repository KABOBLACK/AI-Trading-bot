import pandas as pd

from backtest.backtester import run_backtest


def test_backtester_returns_performance_data():

    data = pd.DataFrame({
        "open": [100 + i for i in range(40)],
        "high": [102 + i for i in range(40)],
        "low": [98 + i for i in range(40)],
        "close": [101 + i for i in range(40)],
        "volume": [1000] * 40
    })

    result = run_backtest(
        data,
        starting_balance=1000
    )

    assert isinstance(result, dict)

    assert "total_trades" in result
    assert "winning_trades" in result
    assert "losing_trades" in result
    assert "profit_loss" in result
    assert "ending_balance" in result
    assert "max_drawdown" in result