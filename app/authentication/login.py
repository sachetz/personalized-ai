import streamlit as st
from time import sleep

from db.mysql.utils import validate_login

def login():
    st.markdown("<h3 style='text-align: center;'>Log In</h3>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username: ")
        password = st.text_input("Password: ", type="password")  # Mask password input
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                id = validate_login(username, password)
                st.session_state.authenticated = True
                st.session_state.user_id = id
                st.session_state.user_name = username
                st.success("Logged in successfully!")
                sleep(0.5)
                st.switch_page("pages/landing.py")
            except Exception as e:
                st.error("Invalid username or password.")
