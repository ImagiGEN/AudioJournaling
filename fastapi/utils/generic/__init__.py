import bcrypt
import time
from jose import jwt
from datetime import datetime, timedelta
import os
import speech_recognition as sr
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def parse_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(access_token):
    decoded_token = jwt.decode(
        access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token


def compare_time(token_time: int):
    if int(time.time()) < token_time:
        return True
    else:
        return False

def get_audio_transcript(audio_file_name):
    # use the audio file as the audio source    
    try:                                    
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_name) as source:
            audio = r.record(source)  # read the entire audio file                  
            transcript = r.recognize_whisper(audio)
            print("Transcription: " + transcript)
    except Exception as e:
        print("Exception:", str(e))
        transcript = ""
    return transcript
