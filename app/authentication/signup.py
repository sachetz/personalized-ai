# authentication/signup.py
import streamlit as st

from db.mysql.utils import register

def signup():
    st.header("Sign Up")

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
                register(new_username, new_password, new_email)
                st.success("Registration successful! You can now log in.")
                st.session_state.current_page = "login"
                st.rerun()
