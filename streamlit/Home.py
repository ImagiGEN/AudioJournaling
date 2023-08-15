import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)
col1, col2, col3 = st.columns(3)
with col2:
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
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

from PIL import Image

image = Image.open('./images/home_page.jpg')
st.image(image)

# Run the app
# streamlit run main.py
