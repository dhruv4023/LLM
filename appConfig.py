import os
import streamlit as st

# class Configurations():
    # MONGO_DB_URL = st.secrets["MONGO_DB_URL"] 
    # AUTH_API_END_POINT = st.secrets["AUTH_API_END_POINT"] 
    
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["env"]["HUGGINGFACEHUB_API_TOKEN"]
