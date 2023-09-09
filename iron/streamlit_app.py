import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from conn import mongo_client as client
from data import get_data


data = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

start, end = st.select_slider(
    "Select a range of dates", options=data.index, value=(min(data.index), max(data.index))
)
attributes_y1 = st.multiselect("Select attributes Y1", data.columns, default=["body_fat"])

attributes_y2 = st.multiselect("Select attributes Y2", data.columns, default=["mass_kg"])

# st.table(filtered_y1.T)

tab1, tab2 = st.tabs(["Line chart", "Bar chart"])

with tab1:
    filtered_y1 = data.loc[(data.index >= start) & (data.index <= end), attributes_y1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = px.line(filtered_y1, markers=True)
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    filtered_y2 = data.loc[(data.index >= start) & (data.index <= end), attributes_y2]
    fig = px.bar(filtered_y2)
    st.plotly_chart(fig, use_container_width=True)
