import pandas as pd
from src.models.schemas import TechnicalAnalysis

class TechnicalAgent:
    def __init__(self, symbol: str = "BTC/USDT"):
        self.symbol = symbol

    def _calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> float:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1])

    def analyze(self, df: pd.DataFrame) -> TechnicalAnalysis:
        rsi = self._calculate_rsi(df)
        
        # Calculate Short/Long Exponential Moving Averages for MACD Signal
        ema12 = df['close'].ewm(span=12, adjust=False).mean()
        ema26 = df['close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        
        macd_val = macd.iloc[-1]
        signal_val = signal.iloc[-1]

        if macd_val > signal_val and rsi < 70:
            macd_signal = "BULLISH"
        elif macd_val < signal_val and rsi > 30:
            macd_signal = "BEARISH"
        else:
            macd_signal = "NEUTRAL"

        summary = f"RSI(14) is {rsi:.2f}. MACD line ({macd_val:.2f}) vs Signal ({signal_val:.2f}) indicates {macd_signal} momentum."

        return TechnicalAnalysis(
            symbol=self.symbol,
            rsi_14=round(rsi, 2),
            macd_signal=macd_signal,
            indicator_summary=summary
        )