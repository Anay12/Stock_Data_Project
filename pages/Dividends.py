import streamlit as st
import yfinance as yf
import pandas as pd
from statsmodels.graphics import tsaplots

from pages.Holdings import read_holdings

holdings_df = read_holdings()

for stock_ticker in holdings_df['Ticker']:
    print(holdings_df.Ticker)

    ticker = yf.Ticker(stock_ticker)
    dividends = ticker.dividends

    eps_trend = ticker.eps_trend
    quarterly_cashflow = ticker.quarterly_cashflow
    ttm_cashflow = ticker.ttm_cashflow


