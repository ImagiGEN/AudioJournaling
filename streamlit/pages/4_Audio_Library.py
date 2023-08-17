import streamlit as st
import pandas as pd
import os
from utils import backend
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def get_journal_history():
    s_date = datetime.combine(start_date, datetime.min.time())
    e_date = datetime.combine(end_date, datetime.max.time())
    response = backend.fetch_journal_history(st.session_state.auth_token, s_date, e_date)
    if response[0]:
        journal_history = response[1]
        audio_files = pd.DataFrame(journal_history)
    else:
        audio_files = pd.DataFrame()
    return audio_files

def get_audio_data(file_url):
    response = backend.fetch_audio_file(st.session_state.auth_token, file_url)
    return response

def get_transcript_and_emotion(audio_id):
    response = backend.fetch_transcript_and_emotion(st.session_state.auth_token, audio_id)
    return response

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

def format_dataframe(audio_df):
    display_df = audio_df.drop(columns=["id", "file_url"])
    display_df["timestamp"] = pd.to_datetime(display_df["timestamp"])
    display_df.style.format({"timestamp": lambda t: t.strftime("%d-%m-%Y:%H:%M:%S")})
    display_df.columns = [col.capitalize() for col in display_df.columns]
    return display_df

auth_user = authentication()

if auth_user[0]:
    st.title("Audio Library")
    st.markdown("Watch your personal audio library unfold - Listen to your recordings by date")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(7), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())
    with col2:
        end_date = st.date_input("End Date", value=datetime.now(), min_value=datetime.now() - timedelta(1000), max_value=datetime.now())

    audio_df = get_journal_history()

    if audio_df.empty:
        st.markdown("No audio files found.")
    else:
        display_df = format_dataframe(audio_df)
        st.write(display_df)

        # Allow user to select an audio file to play
        selected_idx = st.selectbox("Select an audio file to play:", display_df.index)
        selected_row = audio_df.loc[[selected_idx]].iloc[0]
        # Play the selected audio file
        with st.spinner("Downloading audio..."):
            response = get_audio_data(selected_row['file_url'])
            if response[0]:
                st.audio(response[1], format='audio/wav')
            else:
                st.error(f"Error downloading audio journal. Details: {response[1]}", icon="🚨")
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
