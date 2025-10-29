from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# from flask_sqlalchemy import SQLAlchemy
from database import Base, engine, get_db
from models import Holding

app = Flask(__name__)

Base.metadata.create_all(bind=engine)


@app.route('/Holdings')
def holdings():
    db = next(get_db())
    holdings = db.query(Holding).all()
    return render_template('holdings.html', holdings=holdings)

@app.route('/Holdings/add', methods=["POST"])
def add_holding():
    db = next(get_db())
    ticker = request.form["ticker"]
    holding_type = request.form["holding_type"]
    holding_size = request.form["holding_size"]
    date_added = request.form["date_added"]

    new_holding = Holding(ticker=ticker, holding_type=holding_type, holding_size=holding_size, date_added=date_added)
    db.add(new_holding)
    db.commit()

    return redirect(url_for('holdings'))

@app.route('/Holdings/delete')
def delete_holdings():
    db = next(get_db())
    db.delete()

    return redirect(url_for('holdings'))

@app.route('/Holdings/edit')
def edit_holdings():
    return redirect(url_for('holdings'))


@app.route('Dividends')
def dividends():
    pass


@app.route('/Performance')
def performance():
    pass



if __name__ == "__main__":
    app.run(debug=True)



