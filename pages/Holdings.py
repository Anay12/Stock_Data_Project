import sys

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine, text

file_path = "holdings_df.csv"
engine = create_engine("sqlite:///holdings.db")

# class Holdings:
#     def __init__(self):
#         self.holdings = []
if not engine.dialect.has_table(engine.connect(), "holdings"):
    holdings_df = pd.DataFrame(columns=['Ticker', 'Holding Type', 'Holding Size'])
    holdings_df.to_sql("holdings", engine, if_exists="replace", index=False)

with engine.begin() as conn:
    # Add the 'id' column if it doesn't exist
    conn.execute(text("ALTER TABLE holdings ADD COLUMN id INTEGER"))
    # Populate it with unique IDs
    conn.execute(text("UPDATE holdings SET id = rowid"))


    # def get_holdings(self):
    #     return self.holdings
    #
    # def set_holdings(self, holdings):
    #     self.holdings = holdings

# write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
# if write_header:
#     holdings_object = Holdings()
#     holdings = holdings_object.get_holdings()

tab1, tab2 = st.tabs(["Overview", "Add a Holding"])

with tab1:
    # holdings = pd.read_sql_table('test', 'jdbc:postgresql://localhost:5432/postgres')
        try:
            holdings_df = pd.read_sql("SELECT * FROM holdings", engine)

            refresh_pie_chart_button = st.button("Refresh")

            if not holdings_df.empty and refresh_pie_chart_button:
                holdings_df['Holding Size'] = pd.to_numeric(holdings_df['Holding Size'], errors='coerce')
                top_ten_holdings_df = holdings_df.head(10)
                chart = px.pie(top_ten_holdings_df, names='Ticker', values='Holding Size')
                st.plotly_chart(chart)

            else:
                st.info('No holdings found. Add a holding in the first tab.')
        except Exception as e:
            st.error(f"Database error: {e}")

with tab2:
    with st.form("Add a holding form"):
        ticker_input = st.text_input("Add a ticker")
        ticker_type = st.selectbox("This holding is a: ", ("Stock", "Fund", "Other"), index=None, placeholder="Select a Holding Type")
        st.write("You selected:", ticker_type)
        holding_size = st.text_input("Add the number of shares you hold")
        submitted = st.form_submit_button('Add ticker to holdings')

    if submitted and ticker_input and holding_size:
        ticker = yf.Ticker(ticker_input)
        try:
            if ticker.info['regularMarketPrice'] is None:
                st.error("Error. Not a valid ticker.")
            else:
                new_entry = pd.DataFrame([[ticker_input, ticker_type, holding_size]], columns=['Ticker', 'Holding Type', 'Holding Size'])
                # holdings_df = pd.concat([holdings_df, new_entry], ignore_index=True)

                new_entry.to_sql("holdings", engine, if_exists='append', index=False)
                st.success(f"{ticker_input} has been added to your holdings.")
        except Exception as e:
            st.error(f"Error fetching ticker info: {e}")

    with st.expander("🗑️ Delete a Holding"):
        holdings = pd.read_sql("SELECT * FROM holdings", engine)

    if not holdings.empty:
        selected_ticker = st.selectbox("Select a holding to delete:", holdings['Ticker'])

        if st.button("Delete Selected Holding"):
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM holdings WHERE Ticker = :ticker"), {"ticker": selected_ticker})
            st.success(f"{selected_ticker} was deleted.")
    else:
        st.info("You have no holdings to delete.")

    # holdings_df.to_sql('test')

