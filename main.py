import streamlit as st
from app.authentication.authentication import authenticate

st.markdown("<h1 style='text-align: center;'>Welcome to your AI Assistant!</h1>", unsafe_allow_html=True)
if not st.session_state.get("authenticated", False):
    authenticate()
else:
    st.switch_page("pages/landing.py")
