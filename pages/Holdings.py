import streamlit as st

import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.express as px

from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

# file_path = "holdings_df.csv"

metadata = MetaData()

holdings_table = Table(
    "holdings", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Ticker", String),
    Column("Holding Type", String),
    Column("Holding Size", Float),
    Column("Date Added", String)
)

engine = create_engine("sqlite:///holdings.db")
metadata.create_all(engine)

# if not engine.dialect.has_table(engine.connect(), "holdings"):
#     holdings_df = pd.DataFrame(columns=['id', 'Ticker', 'Holding Type', 'Holding Size', 'Date Added'])
#     holdings_df.to_sql("holdings", engine, if_exists="replace", index=False)




def read_holdings():
    return pd.read_sql("SELECT * FROM holdings", engine).set_index('id')


# class Holdings:
#     def __init__(self):
#         self.holdings = []
#
#     # def get_holdings(self):
#     #     return self.holdings
#     #
#     # def set_holdings(self, holdings):
#     #     self.holdings = holdings


# write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
# if write_header:
#     holdings_object = Holdings()
#     holdings = holdings_object.get_holdings()


# holdings_obj = Holdings()

tab1, tab2 = st.tabs(["Overview", "Add a Holding"])

with tab1:
    # holdings = pd.read_sql_table('test', 'jdbc:postgresql://localhost:5432/postgres')
        try:
            holdings_df = read_holdings()

            if not holdings_df.empty:
                st.header("All Holdings")
                st.dataframe(holdings_df)

            refresh_pie_chart_button = st.button("Refresh")

            if not holdings_df.empty or refresh_pie_chart_button:
                holdings_df['Holding Size'] = pd.to_numeric(holdings_df['Holding Size'], errors='coerce')
                chart = px.pie(holdings_df, names='Ticker', values='Holding Size')
                st.plotly_chart(chart)

            else:
                st.info('No holdings found. Add a holding in the first tab.')
        except Exception as e:
            st.error(f"Database error: {e}")

with tab2:
    # UI for adding a holding
    with st.form("Add a holding form"):
        ticker_input = st.text_input("Add a ticker")
        ticker_type = st.selectbox("This holding is a: ", ("Stock", "Fund", "Other"), index=None, placeholder="Select a Holding Type")
        st.write("You selected:", ticker_type)
        holding_size = st.text_input("Add the number of shares you hold")
        submitted = st.form_submit_button('Add ticker to holdings')

    # add a holding if the holding is a valid ticker
    if submitted and ticker_input and holding_size:
        ticker = yf.Ticker(ticker_input)
        try:
            if ticker.info['regularMarketPrice'] is None:
                st.error("Error. Not a valid ticker.")
            else:
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                new_entry = pd.DataFrame([[ticker_input, ticker_type, holding_size, current_date]],
                                         columns=['Ticker', 'Holding Type', 'Holding Size', 'Date Added'])
                # holdings_df = pd.concat([holdings_df, new_entry], ignore_index=True)
                # new_entry['id'] = int(pd.read_sql("SELECT MAX(id) FROM holdings", engine).iloc[0, 0] or 0) + 1
                new_entry.to_sql("holdings", engine, if_exists='append', index=False)
                st.success(f"{ticker_input} has been added to your holdings.")
        except Exception as e:
            st.error(f"Error fetching ticker info: {e}")

    # delete a holding
    with st.expander("🗑️ Delete a Holding"):
        holdings_df = pd.read_sql("SELECT * FROM holdings", engine).set_index('id')

    if not holdings_df.empty:
        st.dataframe(holdings_df)

        holdings_df['label'] = holdings_df.apply(
            lambda row: f"Holding: {row['Ticker']}  |  Shares: {row['Holding Size']}", axis=1
        )
        label_to_id = dict(zip(holdings_df['label'], holdings_df.index))

        selected_label = st.selectbox("Select a holding to delete:", list(label_to_id.keys()))
        selected_id = label_to_id[selected_label]


        if st.button("Delete Holding"):
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM holdings WHERE id = :id"), {"id": selected_id})
            st.success(f"Holding ID {selected_id} deleted.")
    else:
        st.info("You have no holdings to delete.")


