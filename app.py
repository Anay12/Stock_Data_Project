from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from sqlalchemy import select

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from Database.database import SessionLocal, engine
from Database.models import Holding
from stock import Stock
from data_retrieval import retrieve_dividends, prices_OHLC

app = Flask(__name__)

app.config.from_mapping({
    'CACHE_TYPE': "SimpleCache",
    'CACHE_DEFAULT_TIMEOUT': 300
})

cache = Cache(app)

@app.context_processor
def inject_active_page():
    return {"active_page": request.endpoint}

@app.route('/')
@cache.cached()
def index():
    # News panel

    # Portfolio breakdown by type
    # classification ['Aggressive growth', 'Growth', 'Balanced', 'Conservative', 'Very conservative']

    return render_template('index.html')

@app.route('/Holdings')
@cache.cached()
def holdings():
    with SessionLocal() as db:
        # with db.begin():
        stmt = select(Holding).options(joinedload(Holding.ticker))
        holdings_table = db.execute(stmt).scalars().all()

        for holding in holdings_table:
            # stock = Stock(holding.ticker.ticker_name)
            # current_price = stock.fetch_price()
            price_diff = holding.ticker.current_price - holding.purchase_price
            holding.exact_gain = price_diff * holding.holding_size
            holding.percent_gain = price_diff / holding.purchase_price
    db.commit()

    ticker_holdings = defaultdict(list)
    for holding in holdings_table:
        ticker_holdings[holding.ticker.ticker_name].append(holding)


    with engine.connect() as conn:
        query = select(Holding.holding_id,
                       Holding.holding_size,
                       Ticker.ticker_name).join(
            Ticker, Ticker.ticker_id == Holding.ticker_id)
        holdings_df = pd.read_sql(query, conn)

    fig = px.pie(holdings_df, names='ticker_name', values='holding_size', hole=0.3)
    holdings_pie = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return render_template('Holdings.html', holdings=holdings_table, holdings_pie=holdings_pie, ticker_holdings=ticker_holdings)

@app.route('/Holdings/refresh-prices', methods=["POST"])
def refresh_prices():
    with SessionLocal() as db:
        with db.begin():
            tickers_table = db.query(Ticker).all()

            for ticker in tickers_table:
                stock = Stock(ticker.ticker_name)
                current_price = stock.fetch_price()
                ticker.current_price = current_price

    return redirect(url_for('holdings'))

@app.route('/Holdings/add', methods=["POST"])
def add_holding():
    ticker_name = request.form["ticker_name"].strip().upper()
    holding_type = request.form["holding_type"]
    holding_size = float(request.form["holding_size"])
    purchase_price = request.form["purchase_price"]
    # date_added = request.form["date_added"]
    # date_py = datetime.strptime(date_added, "%Y-%m-%d")
    date_added = datetime.now()

    with SessionLocal() as db:
        with db.begin():
            # validate ticker name
            stock=Stock(ticker_name)
            if stock.is_valid_ticker():
                ticker = db.query(Ticker).filter(Ticker.ticker_name == ticker_name).first()

                # add new tickers to Ticker table
                if not ticker:
                    ticker = Ticker(ticker_name=ticker_name, holding_type=Stock(ticker_name).get_holding_type())
                    db.add(ticker)
                    db.flush()

                # TODO eventually replace this with 'buy' screen that automatically gets price at purchase time or
                #  some other method of getting accurate purchase price
                # if no purchase price provided, use last market price
                # (included for compatability reasons, not for final use)
                if not purchase_price:
                    purchase_price = stock.fetch_price()
                else:
                    purchase_price = float(purchase_price)

            # TODO get account type from UI (store account type) and automatically associate holdings with account
            # set account to 'Default' if no accounts exist
            account = db.query(Account).first()

            if not account:
                account = Account(account_name="Default", account_type='Unknown')
                db.add(account)
                db.flush()

            # add new holding to Holdings table
            new_holding = Holding(ticker_id=ticker.ticker_id, holding_size=holding_size, purchase_price=purchase_price,
                                  account_name=account.account_name, date_added=date_added)
            db.add(new_holding)

    return redirect(url_for('holdings'))

@app.route('/Holdings/edit', methods=["POST"])
def edit_holdings():
    holding_id = int(request.form["holding_id"])
    ticker_name = request.form["ticker_name"]
    holding_type = request.form["holding_type"]
    holding_size = request.form["holding_size"]
    date_edited = datetime.now()

    with SessionLocal() as db:
        with db.begin():
            holding = db.get(Holding, holding_id)
            # db.query(Holding).get(holding_id)

            try:
                if holding:
                    holding.ticker.ticker_name = ticker_name
                    holding.ticker.holding_type = holding_type
                    holding.holding_size = holding_size
                    holding.date_edited = date_edited
            except Exception as e:
                print(f"Could not add holding: {e}")

    return redirect(url_for('holdings'))

@app.route('/Holdings/delete/<int:holding_id>', methods=["POST"])
def delete_holdings(holding_id):
    with SessionLocal() as db:
        with db.begin():
            holding = db.get(Holding, holding_id)
            if holding:
                db.delete(holding)
    #       add error catching for holding not found/nonexistent

    return redirect(url_for('holdings'))

@app.route('/Dividends')
@cache.cached(timeout=300)
def dividends():
    dividends_df = retrieve_dividends()

    fig = px.line(data_frame=dividends_df, x='Date', y='Dividends', color='Company', markers=True)
    dividends_line_chart = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    dividends_table_html = dividends_df.to_html(classes="table table-bordered", index=False)

    return render_template('Dividends.html', dividends_html=dividends_table_html, dividends_line_chart=dividends_line_chart)

@app.route('/Performance')
@cache.cached()
def performance():

    return render_template('Performance.html')

@app.route('/Prices')
# @cache.cached()
def prices():
    prices_df = prices_OHLC()

    fig = px.line(data_frame=prices_df, x='Date', y='Close', color='Company', markers=True)
    # fig.update_layout(template="plotly_white", hovermode="x unified")

    prices_line_chart = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    prices_table_html = prices_df.to_html(classes="table table-bordered", index=False)

    return render_template('Prices.html', prices_table_html=prices_table_html,
                           prices_line_chart=prices_line_chart)


if __name__ == "__main__":
    app.run(debug=True)



