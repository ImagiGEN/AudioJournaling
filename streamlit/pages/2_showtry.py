import streamlit as st
import numpy as np
import soundfile as sf
import os
from pages.uploadtry import get_session_state

def show_audio_page():
    st.title("Audio Page")
    
    st.write("This is the listing for uploaded audio.")
    session_state = get_session_state()

    # Check if there are uploaded audios
    if session_state.uploaded_audios:
        for idx, audio_info in enumerate(session_state.uploaded_audios):
            temp_file = f"temp_audio_{idx}.wav"
            sf.write(temp_file, audio_info["audio_data"], audio_info["sample_rate"])
            st.audio(temp_file, format='audio/wav', start_time=0)
            st.text(f"Uploaded Audio {idx + 1}")
            os.remove(temp_file) 
    else:
        st.write("No audio uploaded.")

    st.write("This is the listing for recorded audio.")
    session_state = get_session_state()

    if session_state.live_audios:
        for idx, audio_info in enumerate(session_state.live_audios):
            
            temp_file1 = f"temp_audio_{idx}.wav"
            if audio_info["audio_data"] is not None:
                audio_data = audio_info["audio_data"]
                if len(audio_data.shape) == 1:
                    audio_data = np.column_stack((audio_data, audio_data))

                sf.write(temp_file1, audio_data, audio_info.get("sample_rate", 44100))
                st.audio(temp_file1, format='audio/wav', start_time=0)
                st.text(f"Recorded Audio {idx + 1}")
                os.remove(temp_file1) 
    else:
        st.write("No audio recorded.")
show_audio_page()