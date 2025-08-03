# Stock_Analysis
Basic Stock Analysis with SMA and RSI

# Stock SMA & RSI Dashboard

## Description
This project is a web-based dashboard that allows users to analyze stock prices using technical indicators like Simple Moving Average (SMA) and Relative Strength Index (RSI). Users can select a stock symbol and time period to visualize price trends and momentum.

## Technologies and Libraries
- Python 3.x
- Streamlit (for interactive dashboard)
- yfinance (for fetching stock data)
- pandas (for data manipulation)
- matplotlib (for plotting charts)

## Code Structure
  - Imports required libraries.
  - Defines user input controls (stock symbol, analysis period).
  - Fetches stock data using yfinance.
  - Calculates SMA and RSI based on dynamic windows.
  - Displays interactive charts and data tables.
  - Provides CSV download functionality.

## Key Components
- fetch_data(symbol): Download stock data and retrieves company name.
- SMA calculation: Rolling mean over user-defined window to smooth prices.
- RSI calculation: Measures stock momentum to indicate overbought or oversold conditions.
- Streamlit UI: Sidebar for inputs, main page for charts and data display.

## How to Run

1. Install dependencies:
   pip install streamlit yfinance pandas matplotlib
   pip install matplotlib

2. Run the Streamlit app:
   streamlit run stock_details.py
  
3. Open the URL shown in your browser (usually http://localhost:8501)

