import streamlit as st
from time import sleep


def make_sidebar():
    with st.sidebar:
        if st.session_state.get("authenticated", False):
            st.title(st.session_state.user_name + "'s AI 🧑‍💻")
            st.write("")
            st.page_link("pages/chat.py", label="Chat", icon="💬")
            st.page_link("pages/integrations.py", label="Integrations", icon="🔗")
            st.write("")
            if st.button("Log out"):
                logout()
        else:
            st.write("Unauthorized Access")


def logout():
    st.session_state.authenticated = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("main.py")