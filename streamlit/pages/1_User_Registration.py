import streamlit as st
from dotenv import load_dotenv
from utils import backend

load_dotenv()

st.set_page_config(
    page_title="SoundJot",
    page_icon="👋",
)

st.title("User Registration")

def register_user():
    response = backend.create_user(username, password, cnf_password, firstname, lastname)
    if response.get("username"):
        return True

st.subheader("Create an Account")

firstname = st.text_input('First Name')
lastname = st.text_input('Last Name')
username = st.text_input('Username')
password = st.text_input('Password', type='password')
cnf_password = st.text_input('Confirm Password', type='password')
if st.button("Sign Up"):
    if register_user():
        st.success('User Registered Successfully!', icon="✅")
    else:
        st.error('There was an error', icon="🚨")

# Run the app
# streamlit run main.py
