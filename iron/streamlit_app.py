import streamlit as st
import pandas as pd
from pandas import DataFrame
from pymongo import MongoClient


@st.cache_resource
def init_connection():
    user = st.secrets.mongo.user
    password = st.secrets.mongo.password
    return MongoClient(
        f"mongodb+srv://{user}:{password}@pump.u3anmtq.mongodb.net/?retryWrites=true&w=majority"
    )


def to_date(df):
    df["date"] = df["date"].dt.date
    return df


def prepare_data(df: DataFrame) -> DataFrame:
    columns = {
        "dataOrdem": "date",
        "massa": "mass_kg",
        "gc": "body_fat",
        "massaLivre": "free_of_fat_mass_kg",
        "peso_g": "fat_mass_kg",
        "estatura": "height_m",
        "somatorio": "body_folds_sum_mm",
        "c_torax": "chest_cm",
        "c_ombro": "shoulder_cm",
        "c_cintura": "waist_cm",
        "c_abdomen": "abdomen_cm",
        "c_quadril": "hip_cm",
    }
    return (
        df.rename(columns=columns).pipe(to_date).drop(columns={"_id"}).set_index("date")
    )


@st.cache_data(ttl=600)
def get_data(_client, _user_id) -> DataFrame:
    where = {"user_id": _user_id}
    select = {
        "dataOrdem": 1,
        "massa": 1,
        "gc": 1,
        "massaLivre": 1,
        "peso_g": 1,
        "estatura": 1,
        "somatorio": 1,
        "c_torax": 1,
        "c_ombro": 1,
        "c_cintura": 1,
        "c_abdomen": 1,
        "c_quadril": 1,
    }
    anthropometry = _client.pump.anthropometry
    items = anthropometry.find(where, select)
    return prepare_data(pd.DataFrame(data=list(items)))


client = init_connection()

df = get_data(client, "107721031806")

st.title("Anthropometry dashboard")

attributes = st.multiselect("Select attributes", df.columns, default=["body_fat"])

start, end = st.select_slider(
    "Select a range of dates", options=df.index, value=(min(df.index), max(df.index))
)

df_ = df.loc[(df.index >= start) & (df.index <= end), attributes]
st.table(df_.T)

st.line_chart(df_)
