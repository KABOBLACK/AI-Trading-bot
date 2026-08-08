import pandas as pd
from strategy.strategy import generate_signal


def test_strategy_returns_valid_signal():

    data = pd.DataFrame({
        "close": [
            100, 101, 102, 103, 104,
            105, 106, 107, 108, 109,
            110, 111, 112, 113, 114,
            115, 116, 117, 118, 119,
            120, 121, 122, 123, 124,
            125, 126, 127, 128, 129,
            130
        ]
    })

    signal = generate_signal(data)

    assert signal in ["BUY", "SELL", "HOLD"]