import streamlit as st
from utils import backend
import plotly.express as px
from datetime import datetime, timedelta

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
    st.title("Daily Journal")
    selected_date = st.date_input("Select a Date", value=datetime.now(), min_value=datetime.now() - timedelta(1000), max_value=datetime.now()+timedelta(1))
    if st.button("Show"):
        response = get_journal_daily()
        if response[0]:
            st.success('Your journal for the date!')
            st.write(response[1])
        else:
            st.error(f"Error getting your journal for the date. Details: {response[1]}", icon="🚨")
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
