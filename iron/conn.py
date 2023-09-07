import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def init_connection():
    host = st.secrets.mongo.host
    user = st.secrets.mongo.user
    password = st.secrets.mongo.password
    return MongoClient(host.format(user, password))


mongo_client = init_connection()
