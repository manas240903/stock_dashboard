import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="🔄 Sector Rotation Screener", layout="wide")
st.title("🔄 Sector Rotation Dashboard")

sectors = {
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY REALTY": "^CNXREALTY",
    "NIFTY FIN SERVICE": "^NSEFIN"
}

benchmark = "^NSEI"  # NIFTY 50

timeframes = {
    "1 Week": 7,
    "1 Month": 30,
    "3 Months": 90
}

returns_data = []

for name, symbol in sectors.items():
    for label, days in timeframes.items():
        end = date.today()
        start = end - timedelta(days=days)
        data = yf.download(symbol, start=start, end=end, interval="1d")
        if not data.empty:
            start_price = data["Close"].iloc[0]
            end_price = data["Close"].iloc[-1]
            pct_return = ((end_price - start_price) / start_price) * 100
            returns_data.append({"Sector": name, "Timeframe": label, "Return (%)": round(pct_return, 2)})

returns_df = pd.DataFrame(returns_data)

st.subheader("📊 Sector-Wise Returns")
st.dataframe(returns_df.pivot(index="Sector", columns="Timeframe", values="Return (%)").style.background_gradient(cmap='RdYlGn'))

# 📈 Chart
chart = px.bar(
    returns_df,
    x="Sector",
    y="Return (%)",
    color="Timeframe",
    barmode="group",
    title="📈 Sector Rotation Comparison"
)
st.plotly_chart(chart, use_container_width=True)
