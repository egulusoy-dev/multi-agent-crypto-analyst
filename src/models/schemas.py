from pydantic import BaseModel, Field
from typing import Literal

class TechnicalAnalysis(BaseModel):
    symbol: str
    rsi_14: float
    macd_signal: Literal["BULLISH", "BEARISH", "NEUTRAL"]
    indicator_summary: str

class SentimentAnalysis(BaseModel):
    symbol: str
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)  # Range from -1.0 to +1.0
    key_drivers: list[str]

class TradeDecision(BaseModel):
    symbol: str
    action: Literal["BUY", "SELL", "HOLD"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    position_size_usd: float
    stop_loss_price: float
    reasoning: str