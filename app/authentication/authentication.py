import streamlit as st

def authenticate():
    st.header("Welcome! Please choose an option:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Log In"):
            st.session_state.current_page = "login"
            st.rerun()  # Trigger rerun to update the view

    with col2:
        if st.button("Sign Up"):
            st.session_state.current_page = "signup"
            st.rerun()  # Trigger rerun to update the view
