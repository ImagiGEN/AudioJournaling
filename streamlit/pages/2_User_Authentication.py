import streamlit as st
from dotenv import load_dotenv
from utils import backend

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="👋",
)

st.title("User Authentication")

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
    st.write(f"Welcome {auth_user[1]}!!")
    if st.button("Sign Out"):
        st.session_state.auth_token = None
        st.experimental_rerun()
else:
    st.subheader("Sign In")
    username = st.text_input('Username')
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
