import os
import streamlit as st

MONGO_DB_URL = st.secrets["MONGO_DB_URL"]   
MONGO_DB_NAME = st.secrets["MONGO_DB_NAME"]   
MONGO_DB_NAME_CACHE = st.secrets["MONGO_DB_NAME_CACHE"]

os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["env"]["HUGGINGFACEHUB_API_TOKEN"]
