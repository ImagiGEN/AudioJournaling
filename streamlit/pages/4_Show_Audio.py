import streamlit as st
import os
from utils import backend

def list_audio_files():
    audio_files = [f for f in os.listdir('.') if f.endswith('.mp3') or f.endswith('.wav')]
    return sorted(audio_files, reverse=True) 

def get_journal_history():
    journal_history = backend.fetch_journal_history(st.session_state.auth_token)
    audio_files = [f"{journal['id']}:{journal['file_url']}" for journal in journal_history]
    return audio_files

def get_audio_data(file_url):
    file_name = backend.fetch_file_gcs(file_url)
    return file_name

st.title("List of Audio Files")

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user:
    audio_files = get_journal_history()
    if audio_files:
        st.write("Audio Journal History")
        for idx, audio_file in enumerate(audio_files):
            st.write(f"{audio_file}")

        # Allow user to select an audio file to play
        selected_idx = st.selectbox("Select an audio file to play:", audio_files)
        selected_file = audio_files
        downloaded_file = get_audio_data(selected_idx.split(":")[-1])
        st.write(f"Playing audio file: {selected_idx}")
        st.audio(downloaded_file, format='audio/wav')
    else:
        st.write("No audio files found.")
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
