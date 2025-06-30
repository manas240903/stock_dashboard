import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(page_title="📈 Stock Analysis", layout="wide")
st.title("📊 Stock Technical Analysis Dashboard")

ticker = st.text_input("Enter Stock Symbol (e.g. RELIANCE.NS)", "RELIANCE.NS")

if ticker:
    data = yf.download(ticker, period="6mo", interval="1d")

    # SMA 20
    data["SMA_20"] = data["Close"].rolling(window=20).mean()

    # RSI (manual)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Chart
    st.subheader("Price Chart + SMA 20")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_20"], name="SMA 20"))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("RSI (14)")
    st.line_chart(data["RSI"])
