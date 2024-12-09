import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def make_sidebar():
    with st.sidebar:
        st.title("Personalised AI")
        st.write("")
        st.write("")
        if st.session_state.get("authenticated", False):
            # st.page_link("pages/page1.py", label="Secret Company Stuff", icon="🔒")
            # st.page_link("pages/page2.py", label="More Secret Stuff", icon="🕵️")
            st.write("")
            st.write("")
            if st.button("Log out"):
                logout()


def logout():
    st.session_state.authenticated = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("main.py")