import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from datetime import date
from functions import date_years_ago, yesterday_date
# from Database.models import Holding


class Stock(yf.Ticker):
    def __init__(self, ticker, quantity=0, holding_type=''):
        super().__init__(ticker=ticker)
        self.quantity = quantity
        self.holding_type = holding_type
        self.avg_price = 0

    def is_valid_ticker(self):
        try:
            if self.info:
                return True
        except KeyError as e:
            print(f"{self.ticker} is not a valid ticker. Error: {e}")
            return False

    def fetch_price(self):
        return self.info.get("regularMarketPrice")

    def market_value(self):
        price = self.fetch_price()
        return price * self.quantity

    def total_gain(self):
        price = self.fetch_price()
        return (price-self.avg_price) * self.quantity

    def dividend_yield(self):
        return self.info.get("dividendYield")

    # def to_holding(self):
    #     """ convert to Holding DB object """
    #     return Holding(
    #         ticker=self.ticker_str,
    #         holdingSize=self.quantity,
    #
    #     )

    def prices(self, start_date, end_date):
        """ return prices from startDate to endDate in DataFrame """
        return yf.download(self.ticker, start_date, end_date)

    def output_to_csv(self, func, df):
        path = os.getcwd() + f'/data/{func}_{self.ticker}.csv'

        try:
            match func:
                case 'dividends':
                    df.to_csv(path)
                case 'financials':
                    df.to_csv(path)
                case 'prices':
                    df.to_csv(path)
        except FileNotFoundError:
            print("File not found!")

    def prices_years_ago(self, years):
        """ get price history for 1, 5, 10, ... years """
        return self.prices(date_years_ago(years), date.today())

    def get_holding_type(self):
        try:
            holding_type = self.info.get('quoteType', 'Unknown')    # 'EQUITY', 'ETF', 'MUTUALFUND', 'Index'
        except Exception as e:
            return f"Could not retrieve holding type for {self.ticker}. Error: {e}"
        return holding_type

    def is_fund(self):
        return self.get_holding_type() != 'EQUITY'



class Fund(Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    def get_top_holdings(self):
        """ get top holdings for this fund """
        return self.funds_data.top_holdings



""" Other Methods """

def sector_pe_ratio(self):
    """ Compare sector PE ratio to companies' PE ratios """
    ticker = yf.Ticker("XLV") # SPDR health care
    sector_pe = self.info["trailingPE"]

    company_pe_ratios = []

    holdings = self.get_top_holdings()

    for holding in holdings:
        lookup_holding = yf.Lookup(holding)
        holding_ticker = lookup_holding.get_stock().to_csv('holdings_new_df.csv')

        company_pe_ratios.append(yf.Ticker(holding_ticker).info["trailingPE"])

    plt.plot(company_pe_ratios)


def filter_by_characteristics():
    """ Filter/screen by characteristics or query """
    response = yf.screen("aggressive_small_caps")
    return response



# yfinance.Industry('').top_companies
# yfinance.Industry('').top_growth_companies






if __name__ == "__main__":
    stock = Stock('GOOG')
    stock.output_to_csv('dividends', df=stock.dividends)
    #get_PE_ratio("XLV")

    # fund = Fund("XLV")
    # print(fund.getHoldings())


