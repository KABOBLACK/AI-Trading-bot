import pandas as pd


def load_csv_data(filename):
    """
    Load OHLCV market data from a CSV file.
    """

    data = pd.read_csv(filename)

    required_columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"]
    )

    return data