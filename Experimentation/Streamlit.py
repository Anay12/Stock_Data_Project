import pandas as pd
import numpy as np
import streamlit as st

df = pd.DataFrame({
    'first col': [1, 2, 3],
    'second col': [4, 5, 6]
})

# df

dataframe = pd.DataFrame(np.random.randn(10, 20),
                         columns=('col %d' % i for i in range(20)))
# st.dataframe(dataframe.style.highlight_max(axis=0))
# st.dataframe(dataframe)


chart_data = pd.DataFrame(np.random.randn(20, 3),
                          columns=['a', 'b', 'c'])
# st.line_chart(chart_data)


map_data = pd.DataFrame(np.random.randn(1000, 2) / [50,50] + [37.76, -122.4],
                        columns=['lat', 'lon'])
# st.map(map_data)


# widgets
# x = st.slider('x')
# st.write(x, 'squared is', x * x)

# st.text_input("Your name", key="name")
# st.session_state.name

# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#         np.random.randn(20, 3),
#         columns=['a', 'b', 'c'])
#
#     chart_data

# df = pd.DataFrame({
#     'first col': [1, 2, 3],
#     'second col': [4, 5, 6]
# })
#
# option = st.selectbox("Which number do you like best?",
#                       df['first col'])
#
# 'You selected: ', option

# st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ('Email', 'Home phone', 'Mobile')
# )
#
# st.sidebar.slider('Select a range of values', 0, 100, (25, 75))























