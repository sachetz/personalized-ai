import streamlit as st
from time import sleep
from db.mysql.utils import get_last_sync_at
from app.utils.navigation import make_sidebar
from integrations.google.gmail.sync import sync

make_sidebar()

gmail_last_sync_at = get_last_sync_at(st.session_state.user_id)
st.header("Gmail Integration")
st.write("Last Sync At: " + gmail_last_sync_at.strftime("%c"))
if st.button("Connect/Sync"):
    try:
        st.success("Sync Started")
        sync(st.session_state.user_id, int(gmail_last_sync_at.timestamp()))
        st.success("Sync Completed")
        sleep(0.5)
        st.rerun()
    except Exception as e:
        st.error("Sync Failed")

st.header("Calendar Integration")
if st.button("Connect"):
    pass
