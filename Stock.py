import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
# from Database.models import Holding

class Stock:
    def __init__(self, ticker, quantity=0, holding_type=''):
        self.ticker_str = ticker.upper()
        self.quantity = quantity
        self.holding_type = holding_type
        self.avg_price = 0
        self.ticker = yf.Ticker(self.ticker_str)

    @property
    def last_price(self):
        data = self.ticker.history(period="1d")
        return data["Close"].ilod[-1] if not data.empty else None

    @property
    def market_value(self):
        price = self.last_price
        return None if price is None else price * self.quantity

    @property
    def total_gain(self):
        price = self.last_price
        return None if price is None else (price-self.avg_price) * self.quantity

    def dividend_yield(self):
        return self.get_info().get("dividendYield")

    # def to_holding(self):
    #     """ convert to Holding DB object """
    #     return Holding(
    #         ticker=self.ticker_str,
    #         holdingSize=self.quantity,
    #
    #     )

    # access a single ticker and its data
    def get_info(self):
        return self.ticker.info

    # return past dividends as a Pandas Series
    def get_dividends(self):
        return self.ticker.dividends

    def output_dividends_to_csv(self):
        path = os.getcwd() + f'/data/dividends_{self.ticker.ticker}.csv'
        self.get_dividends().to_csv(path)

    # get financial data (income statement)
    def get_financials(self):
        return self.ticker.financials

    # output financial data for 'ticker' to ticker_financials.csv
    def output_financials_to_csv(self):
        path = os.getcwd() + f'/data/{self.ticker.ticker}_financials.csv'
        self.get_financials().to_csv(path)

    # output price information from startDate to endDate to .csv file
    def prices(self, start_date, end_date):
        prices_df = yf.download(self.ticker.ticker, start_date, end_date)
        prices_df.to_csv('_'.join([self.ticker, 'prices.csv']))



class Fund(Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    # get top holdings for a fund
    def get_holdings(self):
        return self.ticker.funds_data.top_holdings

    def sector_pe_ratio(self, ticker):
        ticker = yf.Ticker("XLV") # SPDR health care
        sector_pe = ticker.info["trailingPE"]

        company_pe_ratios = []

        holdings = self.get_holdings()

        for holding in holdings:
            lookup_holding = yf.Lookup(holding)
            holding_ticker = lookup_holding.get_stock().to_csv('holdings_new_df.csv')

            company_pe_ratios.append(yf.Ticker(holding_ticker).info["trailingPE"])

        plt.plot(company_pe_ratios)


""" Other Methods """

# 10 year price history
def prices_10_years():
    stock = Stock('AAPL')


def date_years_ago(years_ago: int):
    """ return date __ years ago """
    if not isinstance(years_ago, int) or years_ago < 0:
        raise ValueError("Years must be a positive integer")

    return date.today() - relativedelta(years=years_ago)


def filter_by_characteristics():
    """ Filter/screen by characteristics or query """
    response = yf.screen("aggressive_small_caps")
    return response



# yfinance.Industry('').top_companies
# yfinance.Industry('').top_growth_companies






if __name__ == "__main__":
    stock = Stock('GOOG')
    stock.output_financials_to_csv()
    #get_PE_ratio("XLV")

    # fund = Fund("XLV")
    # print(fund.getHoldings())


