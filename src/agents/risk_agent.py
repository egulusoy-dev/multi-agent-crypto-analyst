from src.models.schemas import TechnicalAnalysis, SentimentAnalysis, TradeDecision

class RiskManager:
    def __init__(self, max_portfolio_risk_pct: float = 0.02, account_balance: float = 10000.0):
        self.max_risk_pct = max_portfolio_risk_pct
        self.balance = account_balance

    def evaluate_trade(self, tech: TechnicalAnalysis, sent: SentimentAnalysis, current_price: float) -> TradeDecision:
        # Calculate combined signal score (-1.0 to +1.0)
        tech_score = 1.0 if tech.macd_signal == "BULLISH" else (-1.0 if tech.macd_signal == "BEARISH" else 0.0)
        composite_score = (tech_score * 0.5) + (sent.sentiment_score * 0.5)

        # Decide Action based on score threshold
        if composite_score > 0.3:
            action = "BUY"
            stop_loss = current_price * 0.97  # 3% stop loss
        elif composite_score < -0.3:
            action = "SELL"
            stop_loss = current_price * 1.03  # 3% stop loss for short
        else:
            return TradeDecision(
                symbol=tech.symbol,
                action="HOLD",
                confidence=round(abs(composite_score), 2),
                position_size_usd=0.0,
                stop_loss_price=0.0,
                reasoning="Composite signal confidence too low to trigger execution."
            )

        # Enforce Hard Risk Management (Max 2% total portfolio risk per trade)
        max_loss_usd = self.balance * self.max_risk_pct
        price_risk_pct = abs(current_price - stop_loss) / current_price
        position_size = min(max_loss_usd / price_risk_pct, self.balance * 0.10)

        return TradeDecision(
            symbol=tech.symbol,
            action=action,
            confidence=round(min(abs(composite_score), 1.0), 2),
            position_size_usd=round(position_size, 2),
            stop_loss_price=round(stop_loss, 2),
            reasoning=f"Approved based on Technical Signal ({tech.macd_signal}) and Sentiment Score ({sent.sentiment_score:.2f})."
        )