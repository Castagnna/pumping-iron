import streamlit as st
import pandas as pd
from pymongo import MongoClient

user = "foreigner"
password = "foreigner"
MONGODB_URI = f"mongodb+srv://{user}:{password}@pump.u3anmtq.mongodb.net/?retryWrites=true&w=majority"

mg = MongoClient(MONGODB_URI)

anthropometry = mg.pump.anthropometry

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

cursor = anthropometry.find(where, select)

measurements = list(cursor)

df = pd.DataFrame(data=measurements).drop(columns={"_id"})

st.write("stringggg")
st.write(df)
st.table(df)
