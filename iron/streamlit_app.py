import streamlit as st
from conn import mongo_client as client
from data import get_data
from figures import (
    plot_two_axes_line_chart,
    plot_checkbox_stacked_bar_and_line_chart
)
from widgets import date_checkboxes


data = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

selected_dates = date_checkboxes(data, 5)

plot_checkbox_stacked_bar_and_line_chart(data, selected_dates)

start, end = st.select_slider(
    "Select a range of dates",
    options=data.index,
    value=(sorted(data.index)[2], max(data.index)),
)

filtered = data.loc[(data.index >= start) & (data.index <= end)]

y1 = st.selectbox("Select Y1", data.columns, index=0)
y2 = st.selectbox("Select Y2", data.columns, index=len(data.columns) - 5)
plot_two_axes_line_chart(filtered, y1, y2)
