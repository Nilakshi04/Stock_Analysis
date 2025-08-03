import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock SMA & RSI Dashboard", layout="wide")

# -------------------------------
# Sidebar - User Input
# -------------------------------
st.sidebar.title("📊 Stock Analysis Config")

symbol = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, MSFT)", "AAPL").upper()
days_to_analyze = st.sidebar.slider("Days to Analyze", min_value=30, max_value=180, value=90, step=15)

sma_window = max(5, days_to_analyze // 5)
rsi_window = max(7, days_to_analyze // 10)

# -------------------------------
# Fetch Data
# -------------------------------
@st.cache_data
def fetch_data(symbol):
    ticker = yf.Ticker(symbol)
    company_name = ticker.info.get("shortName", symbol)
    df = ticker.history(period="6mo", interval="1d")
    return df.tail(days_to_analyze), company_name

df, company_name = fetch_data(symbol)

if df.empty:
    st.error("No data found. Please check the stock symbol.")
    st.stop()

# -------------------------------
# Compute SMA and RSI
# -------------------------------
df[f"SMA_{sma_window}"] = df["Close"].rolling(window=sma_window).mean()

delta = df["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=rsi_window).mean()
avg_loss = loss.rolling(window=rsi_window).mean()
rs = avg_gain / avg_loss
df[f"RSI_{rsi_window}"] = 100 - (100 / (1 + rs))
df.dropna(inplace=True)

# -------------------------------
# Dashboard Output
# -------------------------------
st.title(f"{company_name} ({symbol}) Stock Dashboard")
st.markdown(f"Analyzing last **{days_to_analyze} days** with:")
st.markdown(f"- **SMA window**: {sma_window} days")
st.markdown(f"- **RSI window**: {rsi_window} days")

# -------------------------------
# Charts
# -------------------------------
st.subheader("📈 Price & Moving Average")
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df.index, df["Close"], label="Close Price", color="blue")
ax.plot(df.index, df[f"SMA_{sma_window}"], label=f"SMA {sma_window}", color="orange")
ax.set_ylabel("Price (USD)")
ax.set_xlabel("Date")
ax.set_title(f"{symbol} - Closing Price with {sma_window}-Day SMA")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("📊 RSI")
fig2, ax2 = plt.subplots(figsize=(14, 3))
ax2.plot(df.index, df[f"RSI_{rsi_window}"], label=f"RSI {rsi_window}", color="green")
ax2.axhline(70, color='red', linestyle='--', label="Overbought (70)")
ax2.axhline(30, color='purple', linestyle='--', label="Oversold (30)")
ax2.set_ylabel("RSI Value")
ax2.set_xlabel("Date")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# -------------------------------
# Data Table & Download
# -------------------------------
st.subheader("📄 Raw Data")
st.dataframe(df.tail(10), use_container_width=True)

csv = df.to_csv().encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"{symbol}_analysis.csv",
    mime="text/csv",
)
