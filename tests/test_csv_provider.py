from data.csv_provider import CSVDataProvider


def test_csv_provider():

    provider = CSVDataProvider(
        "data/sample_ohlcv.csv"
    )

    data = provider.get_ohlcv(
        symbol="BTCUSDT",
        timeframe="1h",
        limit=10
    )

    assert len(data) == 10

    assert "open" in data.columns
    assert "high" in data.columns
    assert "low" in data.columns
    assert "close" in data.columns
    assert "volume" in data.columns