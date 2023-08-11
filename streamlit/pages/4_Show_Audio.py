import streamlit as st
import os
from utils import backend

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
    
def list_audio_files():
    audio_files = [f for f in os.listdir('.') if f.endswith('.mp3') or f.endswith('.wav')]
    return sorted(audio_files, reverse=True) 

def get_journal_history():
    response = backend.fetch_journal_history(st.session_state.auth_token)
    if response[0]:
        journal_history = response[1]
        audio_files = [f"{journal['id']}:{journal['file_url']}" for journal in journal_history]
    else:
        audio_files = []
    return audio_files

def get_audio_data(file_url):
    response = backend.fetch_audio_file(st.session_state.auth_token, file_url)
    return response

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title("List of Audio Files")
    audio_files = get_journal_history()
    if audio_files:
        st.write("Audio Journal History")
        for idx, audio_file in enumerate(audio_files):
            st.write(f"{audio_file}")

        # Allow user to select an audio file to play
        selected_idx = st.selectbox("Select an audio file to play:", audio_files)
        selected_file = audio_files
        with st.spinner("Downloding audio..."):
            response = get_audio_data(selected_idx.split(":")[-1])
            if response[0]:
                st.success('Here is your audio clip')
                st.audio(response[1], format='audio/wav')
            else:
                st.error(f"Error downloading audio journal. Details: {response[1]}", icon="🚨")
    else:
        st.write("No audio files found.")
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
