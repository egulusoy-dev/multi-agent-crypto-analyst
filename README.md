# Autonomous Multi-Agent Financial Analyst

An end-to-end Python engine that leverages multi-agent signal consensus (Technical Analysis + Sentiment Scoring) guarded by deterministic risk management rules to output verified trading decisions with position sizing.

## Key Features
- **Real-Time Data Extraction**: Fetches exchange candle data via `ccxt`.
- **Technical Indicator Agent**: Computes dynamic RSI(14) and MACD signals using `pandas`.
- **Structured Schemas**: Enforces strict typing and output validation using `pydantic`.
- **Deterministic Risk Engine**: Hard-caps position sizing based on portfolio risk tolerance and stop-loss logic.
- **Interactive UI**: Built-in `Streamlit` dashboard for live visualization.

## Architecture Pipeline
1. `MarketFetcher`: Retrieves real-time price & OHLCV data.
2. `TechnicalAgent`: Analyzes indicator momentum.
3. `SentimentAgent`: Evaluates market sentiment.
4. `RiskManager`: Enforces execution logic and output schemas.

## Quick Start

### Local Setup
```bash
git clone [https://github.com/YOUR_USERNAME/multi-agent-crypto-analyst.git](https://github.com/YOUR_USERNAME/multi-agent-crypto-analyst.git)
cd multi-agent-crypto-analyst
pip install -r requirements.txt
python3 main.py