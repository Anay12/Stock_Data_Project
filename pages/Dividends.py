import streamlit as st
import yfinance as yf
import pandas as pd
import

from pages.Holdings import read_holdings

holdings_df = read_holdings()

for ticker in holdings_df['Ticker']:
    print(holdings_df.Ticker)

    dividends = ticker.dividends

    eps_trend = ticker.eps_trend
    quarterly_cashflow = ticker.quarterly_cashflow
    ttm_cashflow = ticker.ttm_cashflow


