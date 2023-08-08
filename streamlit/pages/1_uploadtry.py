import streamlit as st
import soundfile as sf
import numpy as np
import os
import io
from audio_recorder_streamlit import audio_recorder
# Function to get the session state

def get_session_state():
    if 'uploaded_audios' not in st.session_state:
        st.session_state.uploaded_audios = []
    if 'live_audios' not in st.session_state:
        st.session_state.live_audios = []
    return st.session_state

# Function to calculate audio duration
def get_audio_duration(audio_data):
    y, sr = audio_data
    duration = len(y) / sr
    return duration

page_names = ['UploadAudio', 'RecordAudio'] 
page = st.radio('Select one Aggregate',page_names)
st.write ("return:", page)


def upload_audio_page():
    st.write("This is the upload audio page.")
    session_state = get_session_state()
    audio_data = None

    st.title("Upload Audio")
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])


    if st.button("Submit Uploaded File") and uploaded_file is not None:
       
         try:
            audio_data, sample_rate = sf.read(uploaded_file)
            session_state.uploaded_audios.append({"audio_data": audio_data, "sample_rate": sample_rate})
            audio_duration = get_audio_duration((audio_data, sample_rate))
            st.write(f"Audio Duration: {audio_duration:.2f} seconds")
            st.audio(uploaded_file, format='audio/wav')

         except Exception as e:
            st.error(f"Error reading the audio file: {e}")

        
def upload_live_page():
    st.write('Please click on the microphone to start recording')
    session_state = get_session_state()
    audio_data = None
    audio_bytes = audio_recorder()

    if st.button("Submit Live Audio") and audio_bytes is not None:
        default_sample_rate = 44100
        audio_data, _ = sf.read(io.BytesIO(audio_bytes))

        if audio_data is not None and hasattr(audio_data, 'shape'):
            # Convert mono audio to stereo by duplicating the audio_data along the columns
            if len(audio_data.shape) == 1:
                audio_data = np.column_stack((audio_data, audio_data))
            
            session_state.live_audios.append({"audio_data": audio_data, "sample_rate": default_sample_rate})
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.error("No audio recorded.")



if page == 'UploadAudio':
    upload_audio_page()
else:
    upload_live_page()