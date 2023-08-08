import streamlit as st
import os


def list_audio_files():
    audio_files = [f for f in os.listdir('.') if f.endswith('.mp3') or f.endswith('.wav')]
    return sorted(audio_files, reverse=True) 

st.title("List of Audio Files")

audio_files = list_audio_files()

if audio_files:
    st.write("List of Available Audio Files:")
    for idx, audio_file in enumerate(audio_files, start=1):
        st.write(f"{idx}. {audio_file}")

    # Allow user to select an audio file to play
    selected_idx = st.selectbox("Select an audio file to play:", range(1, len(audio_files) + 1))
    selected_file = audio_files[selected_idx - 1]

    st.write(f"Playing audio file: {selected_file}")
    st.audio(selected_file, format='audio/wav')
else:
    st.write("No audio files found.")
