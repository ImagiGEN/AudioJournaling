import streamlit as st
from utils import backend
import plotly.express as px
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def get_journal_daily():
    s_date = datetime.combine(selected_date, datetime.min.time())
    response = backend.get_journal_by_date(st.session_state.auth_token, s_date)
    return response

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title("Chapters")
    st.markdown("Immerse yourself in chapters of your life!")
    st.divider()
    selected_date = st.date_input("Select a date", value=datetime.now(), min_value=datetime.now() - timedelta(1000), max_value=datetime.now()+timedelta(1))
    if st.button("Get summary"):
        with st.spinner("Loading your day..."):
            response = get_journal_daily()
        if response[0]:
            st.subheader("Summary of the day")
            st.markdown(response[1].get("summary"))
            st.subheader("Your words")
            st.markdown(response[1].get("tanscript"))
        else:
            st.error(f"Error getting your journal for the date. Details: {response[1]}", icon="🚨")
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
