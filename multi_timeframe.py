import streamlit as st
import yfinance as yf
import pandas as pd

st.title("⏳ Multi-Timeframe Performance Viewer")

# Define stocks and timeframes
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "KOTAKBANK.NS", "ITC.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS"
]

timeframes = {
    "1D": 1,
    "1W": 7,
    "1M": 30
}

# User selection
selected_stocks = st.multiselect("📌 Select stocks to analyze", stocks, default=stocks[:5])
performance_data = []

# Fetch and calculate performance
for stock in selected_stocks:
    try:
        df = yf.download(stock, period="2mo", interval="1d")
        row = {"Stock": stock}

        for label, days in timeframes.items():
            if len(df) >= days:
                end_price = df["Close"].iloc[-1]
                start_price = df["Close"].iloc[-days]
                change = ((end_price - start_price) / start_price) * 100
                row[label] = round(change, 2)
            else:
                row[label] = None

        performance_data.append(row)

    except Exception as e:
        st.error(f"🚫 Error fetching data for {stock}: {e}")

# Show results
if performance_data:
    df_perf = pd.DataFrame(performance_data)

    # Highlight only numeric columns
    numeric_cols = ["1D", "1W", "1M"]
    styled_df = df_perf.style.highlight_max(subset=numeric_cols, color="lightgreen") \
                             .highlight_min(subset=numeric_cols, color="salmon")

    st.subheader("📈 Performance Table")
    st.dataframe(styled_df)
else:
    st.warning("⚠️ No data to display.")
