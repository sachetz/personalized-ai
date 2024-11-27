import streamlit as st
from db.mysql.utils import validate_login

def login():
    st.header("Log In")

    with st.form("login_form"):
        username = st.text_input("Username: ")
        password = st.text_input("Password: ", type="password")  # Mask password input
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                id = validate_login(username, password)
                st.session_state.is_authenticated = True
                st.session_state.current_page = "landing"
                st.session_state.id = id
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            except Exception as e:
                st.error("Invalid username or password.")
