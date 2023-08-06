import streamlit as st
import soundfile as sf
import numpy as np
from audio_recorder_streamlit import audio_recorder




# Set the title and other configurations of the Streamlit app
st.title('Audio Journal App')

st.write('Please click on the microphone to start recording')
#Live audio recording
audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
  

# Function to get the duration of the audio
def get_audio_duration(audio_data):
    y, sr = audio_data
    duration = len(y) / sr
    return duration

# Set the title and other configurations of the Streamlit app
st.title('Audio Journal App')

# Add an AudioFileUploader widget
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the uploaded audio file using soundfile
        audio_data, sample_rate = sf.read(uploaded_file)

        # Calculate audio duration
        audio_duration = get_audio_duration((audio_data, sample_rate))

        # Display the audio duration
        st.write(f"Audio Duration: {audio_duration:.2f} seconds")
        
        # Play the audio using st.audio
        st.audio(uploaded_file, format='audio/wav')  # Change the format to 'audio/mp3' for MP3 files


    except Exception as e:
        st.error(f"Error reading the audio file: {e}")
