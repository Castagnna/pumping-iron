import streamlit as st
import pandas as pd
from pymongo import MongoClient


@st.cache_resource
def init_connection():
    user = st.secrets.mongo.user
    password = st.secrets.mongo.password
    return MongoClient(f"mongodb+srv://{user}:{password}@pump.u3anmtq.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()

@st.cache_data(ttl=600)
def get_data():
    where = {"user_id": "107721031806"}
    select = {
        "dataOrdem": 1,
        "massa": 1,
        "gc": 1,
        "massaLivre": 1,
        "peso_g": 1,
        "peso_r": 1,
        "estatura": 1,
        "somatorio": 1,
        'c_torax': 1,
        'c_ombro': 1,
        'c_cintura': 1,
        'c_abdomen': 1,
        'c_quadril': 1,
    }
    anthropometry = client.pump.anthropometry
    items = anthropometry.find(where, select)
    return pd.DataFrame(data=list(items)).drop(columns={"_id"}).set_index("dataOrdem")

df = get_data()

st.title("Anthropometry dashboard")

attributes = st.multiselect(
    'Select attributes',
    df.columns,
    default=["gc"]
)

start, end = st.select_slider(
    'Select a range of dates',
    options=df.index,
    value=(min(df.index), max(df.index))
)

df_ = df.loc[(df.index >= start) & (df.index <= end), attributes]
st.table(df_.T)

st.line_chart(df_)
