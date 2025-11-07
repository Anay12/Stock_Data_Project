import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import select
import plotly.express as px
import plotly.io as pio
from database import SessionLocal, engine
from models import Holding

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
        holdings = db.query(Holding).all()

    with engine.connect() as conn:
        query = select(Holding)
        holdings_df = pd.read_sql(query, conn)

    fig = px.pie(holdings_df, names='ticker', values='holdingSize', hole=0.3)
    holdings_pie = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return render_template('holdings.html', holdings=holdings, holdings_pie=holdings_pie)

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
    id = int(request.form["id"])
    ticker = request.form["ticker"]
    holding_type = request.form["holding_type"]
    holding_size = request.form["holding_size"]
    date_edited = datetime.now()

    with SessionLocal() as db:
        with db.begin():
            holding = db.query(Holding).get(id)
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

    return render_template('Dividends.html')


@app.route('/Performance')
def performance():

    return render_template('Performance.html')



if __name__ == "__main__":
    app.run(debug=True)



