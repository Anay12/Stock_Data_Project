import yfinance
from sklearn.model_selection import train_test_split
import pandas as pd

import statsmodels.tsa.api as tsa
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.stattools import adfuller

# class Data:
#     def __init__(self):
#         self.holdings = []
#
#     def getHoldings(self):
#         return self.holdings
#
#     def setHoldings(self, holdings):
#         self.holdings = holdings


class Stock:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    # access a single ticker and its data
    def getGeneralInfo(self):
        return self.ticker.info

    # return past dividends as a Pandas Series
    def getDividends(self):
        return self.ticker.dividends

    # get financial data (income statement)
    def getFinancialData(self, ticker):
        return self.ticker.financials

    # output financial data for 'ticker' to ticker_financials.csv
    def output_financials_to_csv(self, ticker):
        self.getFinancialData('GOOG').to_csv('_'.join([self.ticker.ticker, 'data/financials.csv']))

    # output price information from startDate to endDate to .csv file
    def getPrices(self, startDate, endDate):
        prices_df = yf.download(self.ticker.ticker, startDate, endDate)
        prices_df.to_csv('_'.join([self.ticker, 'prices.csv']))





class Fund(Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    # get top holdings for a fund
    def getHoldings(self):
        return self.ticker.funds_data.top_holdings

    def get_sector_PE_ratio(self, ticker):
        ticker = yf.Ticker("XLV") # SPDR health care
        sectorPE = ticker.info["trailingPE"]

        company_PE_ratios = []

        holdings = self.getHoldings(self.ticker)

        for holding in holdings:
            lookup_holding = yf.Lookup(holding)
            holding_ticker = lookup_holding.get_stock().to_csv('holdings_new_df.csv')

            company_PE_ratios.append(yf.Ticker(holding_ticker).info["trailingPE"])

        plt.plot(company_PE_ratios)





class OtherMethods:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    # Filter/screen by characteristics or query
    def filter_by_characteristics(self):
        response = yf.screen("aggressive_small_caps")
        print(response)





# yfinance.Industry('').top_companies
# yfinance.Industry('').top_growth_companies









if __name__ == "__main__":
    stock = Stock('GOOG')
    stock.output_financials_to_csv('GOOG')
    #get_PE_ratio("XLV")

    st.dataframe('GOOG')

    fund = Fund("XLV")
    print(fund.getHoldings())


