import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from Stock import Stock

def compute_compound_interest(principal: float, div_yield: float, period, time):
    """ compound interest computation """
    return principal * (1 + (.01 * div_yield/period))**(period * time)



