import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date
from dateutil.relativedelta import relativedelta


def date_years_ago(years_ago: int):
    """ return date __ years ago """
    if not isinstance(years_ago, int) or years_ago < 0:
        raise ValueError("Years must be a positive integer")

    return date.today() - relativedelta(years=years_ago)


def compute_compound_interest(principal: float, div_yield: float, period, time):
    """ compound interest computation """
    return principal * (1 + (.01 * div_yield/period))**(period * time)


def plot_dividends(div_df: pd.DataFrame):
    """ forecast future dividends (and maybe when dividends will increase based on revenue/income/stock price) """
    fig = px.line(data_frame=div_df, x='Date', y='Dividends', color='Company', markers=True)
    fig.show()



