from sklearn.model_selection import train_test_split
import pandas as pd
import statsmodels.tsa
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf


# access a single ticker and its data
def get_data(ticker):
    data = yf.Ticker(ticker)

    # holdings = data.funds_data.top_holdings


    return data.financials


# Filter/screen by characteristics or query
def filter_by_characteristics():
    response = yf.screen("aggressive_small_caps")
    print(response)

# with open('financials.csv', 'w') as file:
#     file.write()

get_data('GOOG').to_csv('financials.csv')

def get_PE_ratio(ticker):
    yf.Ticker("XLV") # SPDR health care 
    sectorPE = yf.Ticker("XLV").info["trailingPE"]

    for








