import streamlit as st
from utils import backend
import plotly.express as px
from datetime import datetime, timedelta

def plotly_chart():
    data = get_user_emotions()
    fig = px.pie(values=data.values(), names=data.keys(), hole=0.5, title='Mood chart')
    return fig

def get_user_emotions():
    s_date = datetime.combine(start_date, datetime.min.time())
    e_date = datetime.combine(end_date, datetime.max.time())
    emotion_data = backend.get_user_emotions(st.session_state.auth_token, s_date, e_date)
    return emotion_data
    
st.title("Mood Chart")

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user:
    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(7), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())
    end_date = st.date_input("End Date", value=datetime.now(), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())
    if st.button("Show"):
        fig = plotly_chart()
        st.plotly_chart(fig)
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
