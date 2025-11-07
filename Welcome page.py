import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from pages.Holdings import read_holdings

holdings_df = read_holdings()


st.set_page_config(
    page_title="Welcome Page"
)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.write('Today')

# temp_dat = pd.DataFrame({
#     'values':['one', 'two', 'three', 'four'],
#     'count':[1, 4, 3, 2]
# })

with col2:
    st.write('Summary')

    # top_ten_holdings_df = temp_dat.iloc[0:9, :]

    # chart = px.pie(top_ten_holdings_df, names='values', values='count')
    # chart = px.pie(temp_dat, names='values', values='count')
    # st.plotly_chart(chart)

    if not holdings_df.empty:
        # get price info
        def message_handler(message):
            print("Received message: ", message)


        # with yf.WebSocket() as webSocket:
        #     webSocket.subscribe(['AAPL', 'MSFT'])
        #     st.write(webSocket.listen(message_handler))



        # group holdings together by ticker


        # for each holding group, sum  price x holding size


        # add to new list? and display




        holdings_df['Holding '].sum('')
        holdings_df['Holding Size'] = pd.to_numeric(holdings_df['Holding Size'], errors='coerce')
        chart = px.pie(holdings_df, names='Ticker', values='Holding Size')
        st.plotly_chart(chart)


with col3:
    st.write('News')



def options(ticker_name):
    ticker = yf.Ticker(ticker_name)

    return ticker.option_chain(ticker.options[0]).calls








