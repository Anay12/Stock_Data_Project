import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
from sqlalchemy import select
from Database.database import engine
from Database.models import Holding, Ticker
from stock import Stock
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def get_holdings_df():
    with engine.connect() as conn:
        query = select(Holding.ticker_id,
                       Ticker.ticker_name).join(
            Ticker, Ticker.ticker_id==Holding.ticker_id)

        holdings_df = pd.read_sql(query, conn)
    return holdings_df

def get_unique_tickers():
    holdings_df = get_holdings_df()
    return holdings_df['ticker_name'].unique()

def fetch_performance(ticker):
    """ Worker function for multiprocessing to fetch 1-day performance for a single ticker"""
    try:
        stock_price_df = yf.download(ticker, period='1mo', progress=False).reset_index()

        if len(stock_price_df) < 2:
            print(f"Insufficient data for {ticker}")
            return None

        today_close_price = float(stock_price_df['Close'].iloc[-1])
        yesterday_close_price = float(stock_price_df['Close'].iloc[-2])
        percent_change = ((today_close_price - yesterday_close_price) / yesterday_close_price) * 100

        return pd.DataFrame({'Ticker':[ticker], '1d_performance':[percent_change]})
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def get_1d_performance() -> pd.DataFrame:
    """
    get 1 day performance for all tickers in database
    :return: pd.DataFrame(columns=['Ticker', '1d_performance'])
    """
    unique_tickers = get_unique_tickers()
    one_day_performance = []

    with ProcessPoolExecutor(max_workers=4) as executor:
        future_to_ticker = {executor.submit(fetch_performance, ticker): ticker for ticker in unique_tickers}

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                df_row = future.result()
                if df_row is not None:
                    one_day_performance.append(df_row)
            except Exception as e:
                print(f"Error calculating 1d performance for {ticker}: {e}")

    if one_day_performance:
        performance_df = pd.concat(one_day_performance, ignore_index=True)
    else:
        performance_df = pd.DataFrame(columns=['Ticker', '1d_performance'])


    return performance_df

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
            ticker = future_to_ticker[future]
            try:
                divs_df = future.result()
                print(f"Successfully added dividend data for {ticker}")
                dividends_list.append(divs_df)
            except Exception as e:
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



