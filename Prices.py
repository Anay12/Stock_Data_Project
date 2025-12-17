import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sqlalchemy import select
from Database.database import engine
from Database.models import Holding
from stock import Stock

# plt.axline()

appl_df = yf.download("AAPL", period="10y", interval="1d")
appl_df

def get_dividends_for_today():
    pass




