import pandas as pd
import yfinance as yf

JEPQ = yf.Ticker('JEPQ')
prices_JEPQ = yf.download('JEPQ')

compound_interest_df = pd.DataFrame(columns=("principal", "rate", ))

principal = 0

# use past data to simulate growth in share price, dividend amt

number_of_shares = 40
dividend_amt_per_share = 0.47

total_dividend = number_of_shares * dividend_amt_per_share
share_price = 56
shares_reinvested = total_dividend / share_price
number_of_shares += shares_reinvested