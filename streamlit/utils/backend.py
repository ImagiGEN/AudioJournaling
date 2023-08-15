import os
from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://api:8095")

headers = {'Content-Type': 'application/json'}

def create_user(username, password, cnf_password, firstname, lastname):
    url = f"{BACKEND_API_URL}/api/v1/user"
    payload = {
        "username": username,
        "password": password,
        "cnf_password": cnf_password,
        "firstname": firstname,
        "lastname": lastname
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("username")
    else:
        return False, response.json().get("detail")

def authenticate_user(username, password):
    url = f"{BACKEND_API_URL}/api/v1/user/authenticate"
    payload  = {
        "username": username,
        "password": password
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("auth_token")
    else:
        return False, response.json().get("detail")

def validate_access_token(access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/access_token"
    if not access_token:
        access_token = ""
    payload  = {
        "access_token": access_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("name")
    else:
        return False, response.json().get("detail")

def create_new_audio(audio_file_name, access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/journal/create"
    if not access_token:
        access_token = ""
    payload  = {
        "access_token": access_token,
    }
    files = {
        "audio_file": (f'{audio_file_name}', open(f'{audio_file_name}', 'rb'), 'audio/wav'),
    }
    response = requests.request("POST", url, data=payload, files=files)
    if response.status_code == 200:
        return True, response.json().get("quote")
    else:
        return False, response.json().get("detail")

def fetch_journal_history(access_token, start_date=datetime.now() - timedelta(5), end_date = datetime.now()):
    url = f"{BACKEND_API_URL}/api/v1/user/journal/history"
    if not access_token:
        access_token = ""
    payload  = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "access_token": access_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")

def get_user_emotions(access_token, start_date=datetime.now() - timedelta(7), end_date=datetime.now()):
    url = f"{BACKEND_API_URL}/api/v1/user/emotion/history"
    if not access_token:
        access_token = ""
    payload  = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "access_token": access_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")

def fetch_audio_file(access_token, file_name):
    url = f"{BACKEND_API_URL}/api/v1/user/journal/audio"
    if not access_token:
        access_token = ""
    payload  = {
        "file_url": file_name,
        "access_token": access_token
    }
    json_payload = json.dumps(payload)
    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        with open("downloaded_audio.wav", "wb") as f:
            f.write(response.content)
        return True, "downloaded_audio.wav"
    else:
        return False, response.json().get("detail")
    
def get_journal_by_date(access_token, selected_date = datetime.now()):
    url = f"{BACKEND_API_URL}/api/v1/user/journal/transcript"
    if not access_token:
        access_token = ""
    payload  = {
        "date": selected_date.isoformat(),
        "access_token": access_token
    }
    print(selected_date.isoformat())
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")
# def generate_suggestion(audio_file, emotion):
#     audio_transcript = get_audio_transcript(audio_file)

# create_user("ashritha@gmail.com", "ashritha", "ashritha", "ashritha", "ashritha")
# jwt_token = authenticate_user("ashritha@gmail.com", "ashritha")[1]
# print(jwt_token)
# print(validate_access_token(jwt_token))
# result = create_new_audio("/Users/sayalidalvi/ashritha/Project_old/audio_journaling/archive/Actor_01/03-01-04-02-01-01-01.wav", jwt_token)
# print(result)
# from datetime import datetime, timedelta
# audio_history = fetch_journal_history(jwt_token, datetime.now() - timedelta(1),datetime.now())
# print(audio_history)
# fetch_file_gcs(audio_history[13]['file_url'])
# result = get_user_emotions(jwt_token)
# print(result)
# path='/Users/rishabhindoria/Documents/GitHub/AudioJournaling/airflow/dags/bucketdata1001_DFA_ANG_XX.wav'
# print(get_similar_audios(path))

# results = get_journal_by_date(jwt_token, datetime.now() + timedelta(1))
# print(results)
