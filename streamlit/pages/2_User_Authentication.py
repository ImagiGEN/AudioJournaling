import streamlit as st
from dotenv import load_dotenv
from utils import backend

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="👋",
)

st.title("User Authentication")

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

def user_login():
    response = backend.authenticate_user(username, password)
    if response:
        st.session_state.auth_token = response
    else:
        st.session_state.auth_token = None

auth_user = authentication()

if auth_user:
    st.write(f"Welcome {auth_user}!!")
    if st.button("Sign Out"):
        st.session_state.auth_token = None
        st.experimental_rerun()
else:
    st.subheader("Sign In")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button("Sign In"):
        user_login()
        if not st.session_state.auth_token:
            st.error('Please enter valid credentials', icon="🚨")
        else:
            st.success('User Logged in Successfully!', icon="✅")
            st.experimental_rerun()

# Run the app
# streamlit run main.py
