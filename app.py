from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_name ="stocks_db"


@app.route('/Holdings')
def holdings():

    return render_template('holdings.html', holdings=holdings)


@app.route('Dividends')
def dividends():
    pass


@app.route('/Performance')
def performance():
    pass





