import streamlit as st
import yfinance as yf

ticker = yf.Ticker("AAPL")

time_period_select = st.segmented_control('Time Period', ['1D', '5D', '1M', '1Y', '5Y'])

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