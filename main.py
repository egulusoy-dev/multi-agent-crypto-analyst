from src.utils.market_fetcher import MarketFetcher
from src.agents.technical_agent import TechnicalAgent
from src.agents.sentiment_agent import SentimentAgent
from src.agents.risk_agent import RiskManager

def run_pipeline(symbol: str = "BTC/USDT"):
    print(f"--- Running Multi-Agent Financial Analyst for {symbol} ---\n")

    # 1. Fetch Market Data
    print("[1/4] Fetching live market data...")
    fetcher = MarketFetcher()
    ohlcv_df = fetcher.fetch_ohlcv(symbol=symbol, timeframe="1h", limit=50)
    current_price = fetcher.fetch_ticker_price(symbol=symbol)
    print(f"Current {symbol} Price: ${current_price:,.2f}")

    # 2. Run Technical Agent
    print("\n[2/4] Running Technical Analysis Agent...")
    tech_agent = TechnicalAgent(symbol=symbol)
    tech_result = tech_agent.analyze(ohlcv_df)
    print(f"RSI(14): {tech_result.rsi_14}")
    print(f"MACD Signal: {tech_result.macd_signal}")

    # 3. Run Sentiment Agent
    print("\n[3/4] Running Sentiment Analysis Agent...")
    sentiment_agent = SentimentAgent(symbol=symbol)
    sentiment_result = sentiment_agent.analyze()
    print(f"Sentiment Score: {sentiment_result.sentiment_score}")

    # 4. Evaluate Risk & Execution Strategy
    print("\n[4/4] Evaluating Risk Rules & Final Execution...")
    risk_manager = RiskManager(max_portfolio_risk_pct=0.02, account_balance=10000.0)
    decision = risk_manager.evaluate_trade(tech_result, sentiment_result, current_price)

    print("\n================ FINAL DECISION ================")
    print(f"Action:            {decision.action}")
    print(f"Confidence:        {decision.confidence * 100:.1f}%")
    print(f"Position Size:     ${decision.position_size_usd:,.2f}")
    print(f"Stop Loss Price:   ${decision.stop_loss_price:,.2f}")
    print(f"Reasoning:         {decision.reasoning}")
    print("================================================")

if __name__ == "__main__":
    run_pipeline()