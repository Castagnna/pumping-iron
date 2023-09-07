import streamlit as st
from conn import mongo_client as client
from data import get_data


data = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

attributes = st.multiselect("Select attributes", data.columns, default=["body_fat"])

start, end = st.select_slider(
    "Select a range of dates", options=data.index, value=(min(data.index), max(data.index))
)

filtered = data.loc[(data.index >= start) & (data.index <= end), attributes]

st.table(filtered.T)

tab1, tab2 = st.tabs(["Line chart", "Bar chart"])

with tab1:
    st.line_chart(filtered)
with tab2:
    st.bar_chart(filtered)
