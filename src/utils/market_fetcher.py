import ccxt
import pandas as pd

class MarketFetcher:
    def __init__(self):
        # Using Kraken to prevent US cloud hosting IP blocks from Binance
        self.exchange = ccxt.kraken({
            'enableRateLimit': True,
        })

    def fetch_ticker_price(self, symbol: str = "BTC/USD") -> float:
        symbol = symbol.replace("/USDT", "/USD")
        ticker = self.exchange.fetch_ticker(symbol)
        return float(ticker['last'])

    def fetch_ohlcv(self, symbol: str = "BTC/USD", timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        symbol = symbol.replace("/USDT", "/USD")
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df