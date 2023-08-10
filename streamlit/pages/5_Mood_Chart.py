import streamlit as st
from utils import backend
import plotly.express as px

def plotly_chart():
    data = get_user_emotions()
    fig = px.pie(values=data.values(), names=data.keys(), hole=0.5, title='Mood chart')
    return fig

def get_user_emotions():
    emotions = {
        "sad": 1,
        "happy": 3,
        "disturbed": 4
    }
    return emotions


st.title("Mood Chart")

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user:
    fig = plotly_chart()
    st.plotly_chart(fig)
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
