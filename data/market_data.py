import pandas as pd


def load_csv_data(filename):
    """
    Load OHLCV market data from a CSV file. Ensures timestamp parsing and chronological order.
    """

    # Try to parse timestamp column during read to keep dtypes consistent
    data = pd.read_csv(filename, parse_dates=["timestamp"])

    required_columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Ensure timestamp is datetime and data is sorted chronologically
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    if data["timestamp"].isna().any():
        raise ValueError("Invalid timestamp values found in CSV")

    data = data.sort_values("timestamp").reset_index(drop=True)

    return data
