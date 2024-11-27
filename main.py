import streamlit as st
from app.authentication.authentication import authenticate
from app.authentication.login import login
from app.authentication.signup import signup
from app.landing import landing

# Initialize session state variables
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "authenticate"

# Main navigation logic
if not st.session_state.is_authenticated:
    if st.session_state.current_page == "authenticate":
        authenticate()
    elif st.session_state.current_page == "login":
        login()
    elif st.session_state.current_page == "signup":
        signup()
else:
    landing()
