import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sqlalchemy import select
from Database.database import engine
from Database.models import Holding
from Stock import Stock

# plt.axline()

appl_df = yf.download("AAPL", period="10y", interval="1d")
appl_df

def get_dividends_for_today():
    pass

def prices_OHLC():
    with engine.connect() as conn:
        holdings_df = pd.read_sql(select(Holding), conn)

    def fetch_prices(ticker):
        stock = Stock(ticker)
        stock_price_df = stock.prices_years_ago(1).reset_index()
        stock_price_df['Company'] = ticker
        stock_price_df.columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'Company']
        return stock_price_df

    prices_list = []
    tickers = holdings_df['ticker'].unique()

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

    return prices_df


