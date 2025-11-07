import streamlit as st
import yfinance as yf
from statsmodels.graphics import tsaplots


ticker = yf.Ticker("AAPL")

time_period_select = st.segmented_control('Time Period', ['1D', '5D', '1M', '1Y', '5Y'])

tickers = ['MSFT', 'AAPL', 'GOOG', 'TSLA', 'NFLX']

df = yf.download(tickers, start='2015-01-01', end='2020-12-31')



if time_period_select == '1D':
    st.write(" 1 Day")
elif time_period_select == '5D':
    st.write(" 5 Days")
elif time_period_select == '1M':
    st.write(" 1 Month")
elif time_period_select == '1Y':
    st.write(" 1 Year")
elif time_period_select == '5Y':
    st.write(" 5 Years")
else:
    st.write("")




    # predictions -- if time period is ____ to _____, predict future prices based on trend
    # (and calculate statistics -- variability, high/low prices, etc.)
    # calculate CI or show confidence of the prediction
    # analyze potential results such as gain/loss with probability of the price occurring

    # calculate overall portfolio risk level (maybe with an input for a loss floor/limit that should not be breached)
    # find potential events/catalysts that could cause or explain price moves (earnings, )


