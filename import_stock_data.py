import yfinance
from sklearn.model_selection import train_test_split
import pandas as pd

import statsmodels.tsa.api as tsa
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.stattools import adfuller

class StockData():
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

# access a single ticker and its data
    def getGeneralInfo(self):
        return self.ticker.info

    def getHoldings(self):
        return self.ticker.funds_data.top_holdings

    def getDividends(self):
        return self.ticker.dividends

    def getFinancialData(self, ticker):
        return self.ticker.financials

    # output financial data for 'ticker' to ticker_financials.csv
    def output_financials_to_csv(self, ticker):
        self.getFinancialData('GOOG').to_csv('_'.join([self.ticker.ticker, 'financials.csv']))


    def getPrices(self, startDate, endDate):
        prices_df = yf.download(self.ticker.ticker, startDate, endDate)
        prices_df.to_csv('_'.join([self.ticker, 'prices.csv']))



# Filter/screen by characteristics or query
def filter_by_characteristics():
    response = yf.screen("aggressive_small_caps")
    print(response)


def get_PE_ratio(ticker):
    yf.Ticker("XLV") # SPDR health care
    sectorPE = yf.Ticker("XLV").info["trailingPE"]

    company_PE_ratios = []

    for holding in yf.Ticker("XLV").funds_data.top_holdings:
        lookup_holding = yf.Lookup(holding)
        holding_ticker = lookup_holding.get_stock().to_csv('holdings.csv')

        company_PE_ratios.append(yf.Ticker(holding_ticker).info["trailingPE"])

    plt.plot(company_PE_ratios)


# yfinance.Industry('').top_companies
# yfinance.Industry('').top_growth_companies








if __name__ == "__main__":
    stock = StockData('GOOG')
    stock.output_financials_to_csv('GOOG')
    #get_PE_ratio("XLV")



