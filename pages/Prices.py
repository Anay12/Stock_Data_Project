import pandas as pd
import yfinance as yf


def message_handler(message):
    print("Received message: ", message)

with yf.WebSocket() as webSocket:
    webSocket.subscribe(['AAPL', 'MSFT'])
    webSocket.listen(message_handler)

def market_info(market_name):
    market = yf.Market(market_name)
    status = market.status
    summary = market.summary
