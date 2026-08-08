import pandas as pd


def generate_signal(data):
    """
    Simple moving-average trading strategy.

    BUY  = short moving average crosses above long moving average
    SELL = short moving average crosses below long moving average
    HOLD = no crossover
    """

    data = data.copy()

    data["short_ma"] = data["close"].rolling(window=10).mean()
    data["long_ma"] = data["close"].rolling(window=30).mean()

    if len(data) < 30:
        return "HOLD"

    previous_short = data["short_ma"].iloc[-2]
    previous_long = data["long_ma"].iloc[-2]

    current_short = data["short_ma"].iloc[-1]
    current_long = data["long_ma"].iloc[-1]

    if previous_short <= previous_long and current_short > current_long:
        return "BUY"

    if previous_short >= previous_long and current_short < current_long:
        return "SELL"

    return "HOLD"