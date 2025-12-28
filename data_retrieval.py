import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
from sqlalchemy import select
from Database.database import engine
from Database.models import Holding, Ticker
from stock import Stock
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_holdings_df():
    with engine.connect() as conn:
        query = select(Holding.ticker_id,
                       Ticker.ticker_name).join(
            Ticker, Ticker.ticker_id==Holding.ticker_id)

        holdings_df = pd.read_sql(query, conn)
    return holdings_df

def retrieve_dividends():
    holdings_df = get_holdings_df()
    dividends_list = []

    def fetch_dividends(ticker):
        stock = Stock(ticker)
        divs_df = stock.dividends.reset_index()
        divs_df['Company'] = ticker
        return divs_df

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_ticker = {executor.submit(fetch_dividends, ticker): ticker for ticker in holdings_df[
            'ticker_name'].unique()}

        for future in as_completed(future_to_ticker):
            try:
                divs_df = future.result()
                ticker = future_to_ticker[future]
                print(f"Successfully added dividend data for {ticker}")
                dividends_list.append(divs_df)
            except Exception as e:
                ticker = future_to_ticker[future]
                print(f"Error fetching dividends for {ticker}: {e}")

    if dividends_list:
        dividends_df = pd.concat(dividends_list, ignore_index=True)
    else:
        dividends_df = pd.DataFrame(columns=['Date', 'Dividends', 'Company'])

    return dividends_df


def prices_OHLC():
    holdings_df = get_holdings_df()

    def fetch_prices(ticker):
        stock = Stock(ticker)
        stock_price_df = stock.prices_years_ago(1).reset_index()
        stock_price_df['Company'] = ticker
        stock_price_df.columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'Company']
        return stock_price_df

    prices_list = []
    tickers = holdings_df['ticker_name'].unique()

    for ticker in tickers:
        try:
            prices_list.append(fetch_prices(ticker))
        except Exception as e:
            print(f"Error fetching prices for {ticker}: {e}")

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     future_to_ticker = {executor.submit(fetch_prices, ticker): ticker for ticker in holdings_df['ticker'].unique()}
    #
    #     for future in as_completed(future_to_ticker):
    #         try:
    #             price_df = future.result()
    #             prices_list.append(price_df)
    #         except Exception as e:
    #             ticker = future_to_ticker[future]
    #             print(f"Error fetching prices for {ticker}: {e}")

    if prices_list:
        prices_df = pd.concat(prices_list, ignore_index=True)
    else:
        prices_df = pd.DataFrame(columns=('Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'Company'))

    # prices_df['Date'] = pd.to_datetime(prices_df['Date'])
    # pivot_prices_df = prices_df.pivot(index='Date', columns='Company', values='Close')

    return prices_df



