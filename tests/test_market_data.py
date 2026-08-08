import pandas as pd
import pytest

from data.market_data import load_csv_data


def test_load_csv_data():

    data = load_csv_data(
        "data/sample_ohlcv.csv"
    )

    assert isinstance(data, pd.DataFrame)

    required_columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for column in required_columns:
        assert column in data.columns


def test_missing_columns():

    bad_data = pd.DataFrame({
        "timestamp": ["2026-01-01"],
        "close": [100]
    })

    filename = "data/test_bad_data.csv"

    bad_data.to_csv(
        filename,
        index=False
    )

    with pytest.raises(ValueError):
        load_csv_data(filename)