import streamlit as st
from dotenv import load_dotenv
from utils.upload import upload_audio_page
from utils.showaudio import show_audio_page


load_dotenv()

st.set_page_config(
    page_title="Home Page",
    page_icon="👋",
)

st.title("SoundJot")

st.markdown(
    """
    The cutting-edge audio journaling application designed to preserve your thoughts, 
    emotions, and cherished moments through seamless voice recording. 
    With intuitive features and secure cloud storage, SoundJot offers a private and immersive journaling experience, 
    enabling you to relive your memories anytime, anywhere.
    """
)

# Initialization
#if 'auth_token' not in st.session_state:
#    st.session_state.auth_token = None
pages = {
    "Upload Audio": upload_audio_page,
    "Audio Page": show_audio_page
}

# Run the app
# streamlit run main.py
