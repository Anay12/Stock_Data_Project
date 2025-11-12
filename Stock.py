import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from datetime import date
from Functions import date_years_ago
# from Database.models import Holding

class Stock:
    def __init__(self, ticker, quantity=0, holding_type=''):
        self.ticker_str = ticker.upper()
        self.quantity = quantity
        self.holding_type = holding_type
        self.avg_price = 0
        self.ticker = yf.Ticker(self.ticker_str)

    def last_price(self):
        data = self.ticker.history(period="1d")
        return data["Close"].ilod[-1] if not data.empty else None

    def market_value(self):
        price = self.last_price
        return None if price is None else price * self.quantity

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

    def get_info(self):
        """ access a single ticker and its data """
        return self.ticker.info

    def get_dividends(self):
        """ return past dividends as a Pandas Series """
        return self.ticker.dividends

    def get_financials(self):
        """ get financial data (income statement) """
        return self.ticker.financials

    def prices(self, start_date, end_date):
        """ return prices from startDate to endDate in DataFrame """
        return yf.download(self.ticker_str, start_date, end_date)

    def output_dividends_to_csv(self):
        path = os.getcwd() + f'/data/dividends_{self.ticker_str}.csv'
        self.get_dividends().to_csv(path)

    def output_financials_to_csv(self):
        """ output financials for 'ticker' to financials_ticker.csv """
        path = os.getcwd() + f'/data/financials_{self.ticker_str}.csv'
        self.get_financials().to_csv(path)

    # def output_prices_to_csv(self):
    #     path = os.getcwd() + f'/data/prices_{self.ticker_str}.csv'
    #     self.prices().to_csv(path)

    def output_to_csv(self, func, df):
        path = os.getcwd() + f'/data/{func}_{self.ticker_str}.csv'

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
        """ 10-year price history """
        date_10_years_ago = date_years_ago(years)
        return self.prices(date.today(), date_10_years_ago)


class Fund(Stock):
    def __init__(self, ticker):
        super().__init__(ticker)

    def get_top_holdings(self):
        """ get top holdings for this fund """
        return self.ticker.funds_data.top_holdings

    def sector_pe_ratio(self):
        """ Compare sector PE ratio to companies' PE ratios """
        ticker = yf.Ticker("XLV") # SPDR health care
        sector_pe = self.ticker.info["trailingPE"]

        company_pe_ratios = []

        holdings = self.get_top_holdings()

        for holding in holdings:
            lookup_holding = yf.Lookup(holding)
            holding_ticker = lookup_holding.get_stock().to_csv('holdings_new_df.csv')

            company_pe_ratios.append(yf.Ticker(holding_ticker).info["trailingPE"])

        plt.plot(company_pe_ratios)


""" Other Methods """


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


