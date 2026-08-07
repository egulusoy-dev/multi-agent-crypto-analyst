from src.models.schemas import SentimentAnalysis

class SentimentAgent:
    def __init__(self, symbol: str = "BTC/USDT"):
        self.symbol = symbol

    def analyze(self, news_headlines: list[str] = None) -> SentimentAnalysis:
        # Mock sentiment score evaluation (-1.0 to +1.0)
        # Can be swapped with OpenAI/LangChain LLM tool calls
        if not news_headlines:
            news_headlines = [
                "Bitcoin holds key support level amidst market stability.",
                "Institutional inflow into crypto funds continues upward trend."
            ]

        # Basic sentiment heuristic for local execution
        score = 0.5  # Moderately bullish
        drivers = ["Institutional inflow growth", "Stable price support"]

        return SentimentAnalysis(
            symbol=self.symbol,
            sentiment_score=score,
            key_drivers=drivers
        )