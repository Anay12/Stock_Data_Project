import pandas as pd
import yfinance as yf
import streamlit as st


def message_handler(message):
    print("Received message: ", message)

tickers = ['MSFT', 'AAPL', 'GOOG', 'TSLA', 'NFLX']

df = yf.download(tickers, start='2015-01-01', end='2020-12-31')
st.dataframe(df)


# with yf.WebSocket(str = 'wss://streamer.finance.yahoo.com/?version=2', verbose=True) as webSocket:
#     webSocket.subscribe(['AAPL', 'MSFT'])
#     webSocket.listen(message_handler)

def market_info(market_name):
    market = yf.Market(market_name)
    status = market.status
    summary = market.summary



