import ccxt
import pandas as pd

class MarketFetcher:
    def __init__(self, exchange_id: str = "binance"):
        self.exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})

    def fetch_ohlcv(self, symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 50) -> pd.DataFrame:
        """Fetches historical OHLCV data and returns a pandas DataFrame."""
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def fetch_ticker_price(self, symbol: str = "BTC/USDT") -> float:
        """Fetches the current ticker price."""
        ticker = self.exchange.fetch_ticker(symbol)
        return float(ticker['last'])