# authentication/signup.py
import streamlit as st
from time import sleep

from db.mysql.utils import register

def signup():
    st.markdown("<h3 style='text-align: center;'>Sign Up</h3>", unsafe_allow_html=True)

    with st.form("signup_form"):
        new_username = st.text_input("Username: ")
        new_password = st.text_input("Password: ", type="password")
        new_email = st.text_input("Email: ")
        confirm_password = st.text_input("Re-enter Password: ", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif not new_username or not new_password or not new_email or not confirm_password:
                st.error("Please fill out all fields.")
            else:
                id = register(new_username, new_password, new_email)
                print(id)
                st.session_state.authenticated = True
                st.session_state.user_id = id
                st.session_state.user_name = new_username
                st.success("Registration successful! Logging you in.")
                sleep(0.5)
                st.switch_page("pages/landing.py")
