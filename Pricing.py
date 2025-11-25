import pandas_datareader as pdr
import matplotlib.pyplot as plt
from Stock import Stock
import yfinance as yf

# plt.axline()

appl_df = yf.download("AAPL", period="10y", interval="1d")
appl_df

def get_dividends_for_today():
    pass





