import streamlit as st
import sys

sys.path.append("..") 

from utils.upload import upload_audio_page
from utils.showaudio import show_audio_page


st.set_page_config(
    page_title="Audio Journaling",
    page_icon="👋",
)
st.title('Audio Journal App')

# Function to show the upload page
#upload_audio_page()


pages = {
    "Upload Audio": upload_audio_page,
    "Audio Page": show_audio_page
}

st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", list(pages.keys()))
pages[selected_page]()
