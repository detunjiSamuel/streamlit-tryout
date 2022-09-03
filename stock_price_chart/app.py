import yfinance as yf
import streamlit as st


st.write("""
# Simple Stock Price App
Shown are the stock closing price and volume of Google! from '2018-5-31' to '2022-5-31'

""")


ticker = 'GOOGL'

tickerData = yf.Ticker(ticker)

tickerPriceHistory = tickerData.history(
    period='1d', start='2018-5-31', end='2022-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
     Closing price 
""")
st.line_chart(tickerPriceHistory.Close)
st.write("""
     Sales volume
""")
st.line_chart(tickerPriceHistory.Volume)
