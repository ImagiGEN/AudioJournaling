import streamlit as st
from dotenv import load_dotenv
from utils import backend
from streamlit_extras.switch_page_button import switch_page

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="🎧",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

def user_login():
    response = backend.authenticate_user(username, password)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title(f"Welcome {auth_user[1].capitalize()}!!")
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("Let your emotions flow through your voice!")
        if st.button("Jot Journal"):
            switch_page("Jot_Journal")
    with col2:
        st.markdown("Relive moments with your recordings!")
        if st.button("Audio Library"):
            switch_page("Audio_Library")
    with col3:
        st.markdown("Immerse yourself in chapters of your life!")
        if st.button("Chapters"):
            switch_page("Chapters")
    with col4:
        st.markdown("Kaleidoscope of your emotions!")
        if st.button("Mood Chart"):
            switch_page("Mood_Chart")
    st.divider()
    if st.button("Sign Out"):
        st.session_state.auth_token = None
        st.experimental_rerun()
else:
    st.title("Sign In")
    username = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button("Sign In"):
        response = user_login()
        if response[0]:
            st.session_state.auth_token = response[1]
            st.success('User Logged in Successfully!', icon="✅")
            st.experimental_rerun()
        else:
            st.error(f'{response[1]}', icon="🚨")

# Run the app
# streamlit run main.py
