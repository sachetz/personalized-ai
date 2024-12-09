import streamlit as st
from app.authentication.login import login
from app.authentication.signup import signup

def authenticate():
    col1, col2 = st.columns(2)
    with col1:
        signup()
    with col2:
        login()