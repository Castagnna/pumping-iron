import streamlit as st
import pandas as pd
from pymongo import MongoClient

user = st.secrets.mongo.user
password = st.secrets.mongo.password

@st.cache_resource
def init_connection():
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
    return pd.DataFrame(data=list(items)).drop(columns={"_id"})

df = get_data()

st.write("stringGgg")
st.write(df)
st.table(df)
