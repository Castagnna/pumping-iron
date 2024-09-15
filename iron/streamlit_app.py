import streamlit as st
from conn import mongo_client as client
from data import get_data
from figures import plot_two_axes_line_chart, plot_stacked_bar_and_line_chart, plot_checkbox_stacked_bar_and_line_chart


data = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

n_columns = 5
columns = st.columns(n_columns)
checkbox_values = []

for i, date in enumerate(data.index):
    col = columns[i % n_columns]
    with col:
        checked = st.checkbox(f"{date}", value=True, key=f"checkbox_{date}")
        checkbox_values.append((date, checked))

selected_dates = [date for date, checked in checkbox_values if checked]

plot_checkbox_stacked_bar_and_line_chart(data, selected_dates)

start, end = st.select_slider(
    "Select a range of dates",
    options=data.index,
    value=(sorted(data.index)[2], max(data.index)),
)

filtered = data.loc[(data.index >= start) & (data.index <= end)]

tab1, tab2 = st.tabs(["Comparison", "Mass and body fat"])
with tab1:
    y1 = st.selectbox("Select Y1", data.columns, index=0)
    y2 = st.selectbox("Select Y2", data.columns, index=len(data.columns) - 5)
    plot_two_axes_line_chart(filtered, y1, y2)
with tab2:
    min_range = st.slider("Select min Y", 0, 70, 70, 5)
    plot_stacked_bar_and_line_chart(filtered, min_range)
