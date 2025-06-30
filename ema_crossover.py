import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="⚡ EMA Crossover Screener", layout="centered")
st.title("⚡ EMA Crossover Screener (50 EMA > 200 EMA)")

nifty_stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "KOTAKBANK.NS", "ITC.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS"
]

crossover_stocks = []

for stock in nifty_stocks:
    try:
        st.write(f"📥 Fetching: {stock}")
        data = yf.download(stock, period="6mo", interval="1d", progress=False)

        if data.empty or len(data) < 200:
            continue

        data["EMA50"] = data["Close"].ewm(span=50).mean()
        data["EMA200"] = data["Close"].ewm(span=200).mean()

        if (
            data["EMA50"].iloc[-2] < data["EMA200"].iloc[-2] and
            data["EMA50"].iloc[-1] > data["EMA200"].iloc[-1]
        ):
            crossover_stocks.append(stock)

    except Exception as e:
        st.error(f"🚫 Error for {stock}: {e}")

st.subheader("✅ Golden Cross Stocks (50 EMA > 200 EMA)")

if crossover_stocks:
    st.success(f"🔎 {len(crossover_stocks)} stocks found:")
    st.write(crossover_stocks)
else:
    st.info("😐 No crossovers found today.")
