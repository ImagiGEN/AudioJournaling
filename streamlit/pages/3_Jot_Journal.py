import streamlit as st
import soundfile as sf
import numpy as np
import io
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from utils import backend
import uuid
from streamlit_extras.switch_page_button import switch_page
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

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
    audio_data = None

    uploaded_file = st.file_uploader("Please upload an audio which best describes your mood today!", type=["mp3", "wav"])

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
                if response[0]:
                    st.success('Noted your journal!', icon="✅")
                    st.success(f'{response[1]}❕', icon='😇')
                else:
                    st.error(f"Error saving your journal. Details: {response[1]}", icon="🚨")
        except Exception as e:
            st.error(f"Error reading the audio file: {e}")

def upload_live_page():
    st.write('To speak yout heart out please click on the microphone and start recording!')
    audio_data = None
    audio_bytes = audio_recorder(text="")

    if audio_bytes is not None:
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))

        if audio_data is not None and hasattr(audio_data, 'shape'):
            
            if len(audio_data.shape) == 1:
                audio_data = np.column_stack((audio_data, audio_data))
            
            st.audio(audio_bytes, format="audio/wav")
            if st.button("Submit Live Audio"): 
                with st.spinner("Saving to Journal..."):
                    response = save_audio(audio_data, sr)
                if response[0]:
                    st.success('Noted your journal!', icon="✅")
                    st.success(f'{response[1]}❕', icon='😇')
                else:
                    st.error(f"Error saving your journal. Details: {response[1]}", icon="🚨")
        else:
            st.error("No audio recorded.")

auth_user = authentication()

if auth_user[0]:
    st.title("Jot Journal")
    st.markdown("Let your emotions flow through your voice!")
    page_names = ['Record', 'Upload'] 
    page = st.radio('', page_names, horizontal=True)
    st.divider()
    st.subheader(page)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if page == 'Upload':
        upload_audio_page()
    else:
        upload_live_page()
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
