import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="📊 Fundamental Screener", layout="wide")
st.title("📊 Fundamental Analysis Screener")

# Stock input
symbol = st.text_input("🔍 Enter Stock Symbol (e.g., INFY.NS):", "INFY.NS")

if symbol:
    st.markdown(f"📥 Fetching data for: **{symbol}**")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # 🧾 Basic Details
        st.header("📌 Basic Details")
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Website:** {info.get('website', 'N/A')}")

        # 💰 Financial Metrics
        st.header("💰 Financial Metrics Summary")
        metrics = {
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "ROE (%)": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else "N/A",
            "Net Profit Margin (%)": info.get("netMargins", 0) * 100 if info.get("netMargins") else "N/A",
            "Debt to Equity": info.get("debtToEquity", "N/A")
        }

        df_metrics = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])
        st.dataframe(df_metrics)

        # 📈 Revenue & Net Income Trend
        st.header("📈 Historical Performance (Annual)")
        financials = ticker.financials

        if not financials.empty:
            st.subheader("🧾 Revenue & Net Income")

            data = pd.DataFrame()
            if "Total Revenue" in financials.index and "Net Income" in financials.index:
                data["Revenue"] = financials.loc["Total Revenue"]
                data["Net Income"] = financials.loc["Net Income"]
                st.line_chart(data.T)
            else:
                st.warning("⚠️ 'Total Revenue' or 'Net Income' data not available.")
        else:
            st.warning("⚠️ No financial data available for this stock.")

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
