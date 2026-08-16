from data.data_provider import MarketDataProvider
from data.market_data import load_csv_data
import os


class CSVDataProvider(MarketDataProvider):
    """
    Market-data provider that reads OHLCV data from a CSV file.
    """

    def __init__(self, filename):
        self.filename = filename

    def get_ohlcv(self, symbol, timeframe, limit=100):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"CSV data file not found: {self.filename}")

        data = load_csv_data(self.filename)

        # Return last 'limit' rows in chronological order
        result = data.tail(limit).reset_index(drop=True)
        return result
