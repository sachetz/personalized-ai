# landing.py
import streamlit as st

def landing():
    st.header("Welcome to your personalized AI!")

    if st.button("Logout"):
        st.session_state.is_authenticated = False
        st.session_state.current_page = "authenticate"
        st.rerun()
