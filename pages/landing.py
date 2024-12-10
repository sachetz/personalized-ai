import streamlit as st
from app.utils.navigation import make_sidebar

make_sidebar()

st.header("Welcome to your Personalized AI!")

st.markdown("""
Before proceeding with the chatbot, please link your applications.

Currently, the assistant supports the following:
- GMAIL
- Google Calendar

Select the integrations tab in the sidebar to continue.
""")
