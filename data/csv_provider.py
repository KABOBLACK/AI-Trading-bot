from data.data_provider import MarketDataProvider
from data.market_data import load_csv_data


class CSVDataProvider(MarketDataProvider):
    """
    Market-data provider that reads OHLCV data from a CSV file.
    """

    def __init__(self, filename):
        self.filename = filename

    def get_ohlcv(self, symbol, timeframe, limit=100):
        data = load_csv_data(self.filename)

        return data.tail(limit).reset_index(drop=True)