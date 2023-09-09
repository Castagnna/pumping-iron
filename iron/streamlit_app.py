import streamlit as st
from conn import mongo_client as client
from data import get_data
from figures import plot_two_axes_line_chart


data = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

start, end = st.select_slider(
    "Select a range of dates",
    options=data.index,
    value=(min(data.index), max(data.index)),
)

y1 = st.selectbox("Select Y1", data.columns, index=0)

y2 = st.selectbox("Select Y2", data.columns, index=len(data.columns)-3)

filtered = data.loc[(data.index >= start) & (data.index <= end)]

tab1, tab2 = st.tabs(["Comparison", "Trend"])
with tab1:
    plot_two_axes_line_chart(filtered, y1, y2)
with tab2:
    plot_two_axes_line_chart(filtered, y1, y2)
