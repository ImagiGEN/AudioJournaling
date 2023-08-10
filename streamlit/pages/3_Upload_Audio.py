import streamlit as st
import soundfile as sf
import numpy as np
import os
import io
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from utils import backend
import uuid

# Function to calculate audio duration
def get_audio_duration(audio_data):
    y, sr = audio_data
    duration = len(y) / sr
    return duration

def save_audio(audio_data, sr=44100):
    file_name = f"{timestamp}_{str(uuid.uuid4())}.wav"
    sf.write(file_name, audio_data, sr)
    response = backend.create_new_audio(file_name, st.session_state.auth_token)
    return response

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

def upload_audio_page():
    st.write("This is the upload audio page.")
    audio_data = None

    st.title("Upload Audio")
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if uploaded_file is not None: 
        try:
            audio_data, sample_rate = sf.read(uploaded_file)
            audio_duration = get_audio_duration((audio_data, sample_rate))
            st.write(f"Audio Duration: {audio_duration:.2f} seconds")
            st.audio(uploaded_file, format='audio/wav')

            # Save the audio file to a local path if the "Submit Uploaded File" button is clicked
            if st.button("Submit Uploaded File"):
                audio_data, sr = sf.read(uploaded_file)
                with st.spinner("Saving to Journal..."):
                    response = save_audio(audio_data, sr)
                st.success('Noted your journal!', icon="✅")
                st.success(f'{response}❕', icon='😇')
        except Exception as e:
            st.error(f"Error reading the audio file: {e}")

def upload_live_page():
    st.write('Please click on the microphone to start recording')
    audio_data = None
    audio_bytes = audio_recorder()

    if audio_bytes is not None:
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))

        if audio_data is not None and hasattr(audio_data, 'shape'):
            
            if len(audio_data.shape) == 1:
                audio_data = np.column_stack((audio_data, audio_data))
            
            st.audio(audio_bytes, format="audio/wav")
            if st.button("Submit Live Audio"): 
                with st.spinner("Saving to Journal..."):
                    response = save_audio(audio_data, sr)
                st.success('Noted your journal!', icon="✅")
                st.success(f'{response}❕', icon='😇')
        else:
            st.error("No audio recorded.")

auth_user = authentication()

if auth_user:
    page_names = ['UploadAudio', 'RecordAudio'] 
    page = st.radio('Select one', page_names)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if page == 'UploadAudio':
        upload_audio_page()
    else:
        upload_live_page()
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
