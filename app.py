from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import select

import os
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.io as pio

from Database.database import SessionLocal, engine
from Database.models import Holding
from Stock import Stock

app = Flask(__name__)

@app.context_processor
def inject_active_page():
    return {"active_page": request.endpoint}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Holdings')
def holdings():
    with SessionLocal() as db:
        holdings_table = db.query(Holding).all()

    with engine.connect() as conn:
        query = select(Holding)
        holdings_df = pd.read_sql(query, conn)

    fig = px.pie(holdings_df, names='ticker', values='holdingSize', hole=0.3)
    holdings_pie = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return render_template('holdings.html', holdings=holdings_table, holdings_pie=holdings_pie)

@app.route('/Holdings/add', methods=["POST"])
def add_holding():
    ticker = request.form["ticker"]
    holding_type = request.form["holding_type"]
    holding_size = request.form["holding_size"]
    # date_added = request.form["date_added"]
    # date_py = datetime.strptime(date_added, "%Y-%m-%d")
    date_added = datetime.now()

    with SessionLocal() as db:
        with db.begin():
            new_holding = Holding(ticker=ticker, holdingType=holding_type, holdingSize=holding_size, dateAdded=date_added)
            db.add(new_holding)

    return redirect(url_for('holdings'))

@app.route('/Holdings/edit', methods=["POST"])
def edit_holdings():
    holding_id = int(request.form["id"])
    ticker = request.form["ticker"]
    holding_type = request.form["holding_type"]
    holding_size = request.form["holding_size"]
    date_edited = datetime.now()

    with SessionLocal() as db:
        with db.begin():
            holding = db.query(Holding).get(holding_id)
            if holding:
                holding.ticker = ticker
                holding.holdingType = holding_type
                holding.holdingSize = holding_size
                holding.dateEdited = date_edited

    return redirect(url_for('holdings'))

@app.route('/Holdings/delete/<int:holding_id>', methods=["POST"])
def delete_holdings(holding_id):
    with SessionLocal() as db:
        with db.begin():
            holding = db.query(Holding).get(holding_id)
            if holding:
                db.delete(holding)
    #       add error catching for holding not found/nonexistent

    return redirect(url_for('holdings'))

@app.route('/Dividends')
def dividends():
    with engine.connect() as conn:
        holdings_df = pd.read_sql(select(Holding), conn)

    dividends_df = pd.DataFrame(columns=['Date','Dividends', 'Company'])

    for ticker in holdings_df['ticker']:
        stock = Stock(ticker)

        divs_df = stock.get_dividends().reset_index()
        divs_df['Company'] = ticker

        dividends_df = pd.concat([dividends_df, divs_df])

    fig = px.line(data_frame=dividends_df, x='Date', y='Dividends', color='Company', markers=True)
    dividends_line_chart = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    dividends_table_html = dividends_df.to_html(classes="table table-bordered", index=False)

    return render_template('Dividends.html', dividends_html=dividends_table_html, dividends_line_chart=dividends_line_chart)


@app.route('/Performance')
def performance():

    return render_template('Performance.html')



if __name__ == "__main__":
    app.run(debug=True)



