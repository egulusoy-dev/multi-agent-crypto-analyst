import streamlit as st
import pandas as pd
from src.utils.market_fetcher import MarketFetcher
from src.agents.technical_agent import TechnicalAgent
from src.agents.sentiment_agent import SentimentAgent
from src.agents.risk_agent import RiskManager

st.set_page_config(page_title="Multi-Agent AI Financial Analyst", layout="wide")

st.title("🤖 Autonomous Multi-Agent Financial Analyst")
st.subheader("Real-Time Crypto Analysis & Risk Engine")

symbol = st.sidebar.selectbox("Select Asset Symbol", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
account_balance = st.sidebar.number_input("Account Balance ($)", value=10000.0, step=1000.0)
max_risk_pct = st.sidebar.slider("Max Portfolio Risk per Trade (%)", 0.5, 5.0, 2.0) / 100

if st.button("Run Multi-Agent Analysis"):
    with st.spinner("Executing agent pipeline..."):
        # Fetch Data
        fetcher = MarketFetcher()
        df = fetcher.fetch_ohlcv(symbol=symbol)
        price = fetcher.fetch_ticker_price(symbol=symbol)

        # Run Agents
        tech_agent = TechnicalAgent(symbol=symbol)
        tech_res = tech_agent.analyze(df)

        sent_agent = SentimentAgent(symbol=symbol)
        sent_res = sent_agent.analyze()

        risk_mgr = RiskManager(max_portfolio_risk_pct=max_risk_pct, account_balance=account_balance)
        decision = risk_mgr.evaluate_trade(tech_res, sent_res, price)

    # Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${price:,.2f}")
    col2.metric("Technical RSI (14)", f"{tech_res.rsi_14}")
    col3.metric("MACD Signal", tech_res.macd_signal)

    st.divider()

    st.subheader("🎯 Execution Decision")
    if decision.action == "BUY":
        st.success(f"**Action:** {decision.action} | Confidence: {decision.confidence * 100:.1f}%")
    elif decision.action == "SELL":
        st.error(f"**Action:** {decision.action} | Confidence: {decision.confidence * 100:.1f}%")
    else:
        st.warning(f"**Action:** {decision.action}")

    st.write(f"**Position Size:** ${decision.position_size_usd:,.2f}")
    st.write(f"**Stop Loss Price:** ${decision.stop_loss_price:,.2f}")
    st.info(f"**Reasoning:** {decision.reasoning}")

    st.subheader("📈 Historical Market Data")
    st.line_chart(df.set_index('timestamp')['close'])