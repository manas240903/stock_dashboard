import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="📊 Breakout Screener", layout="centered")
st.title("📊 Price Breakout Screener (30-Day High)")

nifty_stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "KOTAKBANK.NS", "ITC.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS"
]

breakout_data = []

for stock in nifty_stocks:
    try:
        st.write(f"📥 Checking: {stock}")
        data = yf.download(stock, period="3mo", interval="1d", progress=False)

        if data.empty or len(data) < 30:
            st.warning(f"⚠️ Not enough data for {stock}")
            continue

        recent_high = data['Close'].iloc[-30:].max()
        latest_close = data['Close'].iloc[-1]

        if float(latest_close) >= float(recent_high):
            breakout_data.append({
                "Stock": stock,
                "Latest Close": round(latest_close, 2),
                "30-Day High": round(recent_high, 2),
                "Breakout": "✅ YES"
            })
        elif float(latest_close) >= float(recent_high) * 0.98:
            breakout_data.append({
                "Stock": stock,
                "Latest Close": round(latest_close, 2),
                "30-Day High": round(recent_high, 2),
                "Breakout": "⚠️ Near"
            })

    except Exception as e:
        st.error(f"🚫 Error for {stock}: {e}")

st.subheader("📈 Breakout Candidates")

if breakout_data:
    df = pd.DataFrame(breakout_data)
    st.dataframe(df.reset_index(drop=True))
else:
    st.info("🙁 No breakout stocks found today.")
