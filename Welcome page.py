import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Welcome Page"
)

col1, col2, col3 = st.columns([2,2,1])

with col1:
    st.write('Today')

temp_dat = pd.DataFrame({
    'values':['one', 'two', 'three', 'four'],
    'count':[1, 4, 3, 2]
})

with col2:
    st.write('Summary')

    top_ten_holdings_df = temp_dat.iloc[0:9, :]

    # chart = px.pie(top_ten_holdings_df, names='values', values='count')
    chart = px.pie(temp_dat, names='values', values='count')
    st.plotly_chart(chart)


with col3:
    st.write('News')










