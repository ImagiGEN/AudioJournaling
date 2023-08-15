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

def plotly_chart():
    response = get_user_emotions()
    if response[0]:
        data = response[1]
        fig = px.pie(values=data.values(), names=data.keys(), hole=0.5, title='Mood chart')
        return True, fig
    else: 
        return response

def get_user_emotions():
    s_date = datetime.combine(start_date, datetime.min.time())
    e_date = datetime.combine(end_date, datetime.max.time())
    emotion_data = backend.get_user_emotions(st.session_state.auth_token, s_date, e_date)
    return emotion_data
    
def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title("Mood Chart")
    st.markdown("Kaleidoscope of your emotions!")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(7), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())
    with col2:
        end_date = st.date_input("End Date", value=datetime.now(), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())
    if st.button("Show"):
        response = plotly_chart()
        if response[0]:
            st.plotly_chart(response[1])
        else:
            st.error(f"Error getting your emotion history. Details: {response[1]}", icon="🚨")
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
