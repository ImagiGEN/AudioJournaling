import streamlit as st
import pandas as pd
import os
from utils import backend
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def get_journal_history():
    response = backend.fetch_journal_history(st.session_state.auth_token)
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

auth_user = authentication()

if auth_user[0]:
    st.title("Audio Library")
    st.markdown("Watch your personal audio library unfold - Listen to your recordings by date")
    st.divider()

    audio_df = get_journal_history()

    if audio_df.empty:
        st.markdown("No audio files found.")
    else:
        audio_df.drop(columns=["id"], inplace=True)
        audio_df.columns = [col.capitalize() for col in audio_df.columns]
        st.write(audio_df)

        # Allow user to select an audio file to play
        selected_idx = st.selectbox("Select an audio file to play:", audio_df.index)
        selected_row = audio_df.loc[[selected_idx]].iloc[0]
        # Play the selected audio file
        with st.spinner("Downloading audio..."):
            response = get_audio_data(selected_row['File_url'])
            if response[0]:
                st.audio(response[1], format='audio/wav')
            else:
                st.error(f"Error downloading audio journal. Details: {response[1]}", icon="🚨")
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
