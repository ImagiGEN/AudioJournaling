from utils.db_utils import SessionLocal, crud, schemas, models, engine
from utils.generic import decode_token, get_audio_transcript
from utils.gcp_utils import bucket
from utils.pinecone_utils import get_similar_audios
import os
import uuid
from datetime import datetime, timedelta
from utils.pinecone_utils import get_similar_audios
from utils.generic.llm import generate_suggestions

models.Base.metadata.create_all(bind=engine)

def create_user(username, password, cnf_password, firstname, lastname):
    db = SessionLocal()
    data = {
        "username": username,
        "password": password,
        "cnf_password": cnf_password,
        "firstname": firstname,
        "lastname": lastname
    }
    user = schemas.UserCreate(**data)
    return crud.create_user(db, user).__dict__

def authenticate_user(username, password):
    db = SessionLocal()
    data = {
        "username": username,
        "password": password
    }
    creds = schemas.UserAuthentication(**data)
    return crud.authenticate_user(db, creds)

def validate_access_token(access_token):
    db = SessionLocal()
    return crud.validate_access_token(db, access_token)

def create_new_audio(audio_file_name, access_token):
    db = SessionLocal()
    decoded_info = decode_token(access_token)
    destination_file_name = os.path.join(str(decoded_info.get("user_id")), str(uuid.uuid4()),audio_file_name.split("/")[-1])
    bucket.upload_blob(audio_file_name, destination_file_name)
    data = {
        "file_url": destination_file_name,
        "user_id": decoded_info.get("user_id")
        }
    audio = schemas.UserAudioMetadata(**data)
    db_audio = crud.add_audio_metadata(db, audio)
    transcript, emotion = process_user_audio(destination_file_name)
    data = {
        "audio_id": db_audio.id,
        "emotion": emotion
    }
    user_input = schemas.UserAudioEmotion(**data)
    crud.set_emotion_user_audio(db, user_input)
    return generate_suggestions(transcript, emotion)


def fetch_journal_history(access_token, start_date=datetime.now() - timedelta(5), end_date = datetime.now()):
    db = SessionLocal()
    decoded_info = decode_token(access_token)
    data = {
        "start_date": start_date,
        "end_date" : end_date,
        "user_id": decoded_info.get("user_id")
    }
    user_input = schemas.UserAudioHistory(**data)
    return crud.get_journal_history(db, user_input)

def fetch_file_gcs(file_url):
    file_name = bucket.download_as_file(file_url)
    return file_name

def process_user_audio(file_url):
    local_file_name = fetch_file_gcs(file_url)
    transcript = get_audio_transcript(local_file_name)
    audio_ids = get_similar_audios(local_file_name)
    db = SessionLocal()
    data = {
        "audio_path": audio_ids[0] 
    }
    user_input = schemas.DatasetAudio(**data)
    emotion = crud.get_emotion_audio_data(db, user_input)
    return transcript, emotion

# def generate_suggestion(audio_file, emotion):
#     audio_transcript = get_audio_transcript(audio_file)

# create_user("ashritha@gmail.com", "ashritha", "ashritha", "ashritha", "ashritha")
# jwt_token = authenticate_user("ashritha@gmail.com", "ashritha")
# print(validate_access_token(jwt_token))
# result = create_new_audio("/Users/sayalidalvi/ashritha/Project_old/audio_journaling/archive/Actor_01/03-01-04-02-01-01-01.wav", jwt_token)
# print(result)
# from datetime import datetime, timedelta
# audio_history = fetch_journal_history(jwt_token, datetime.now() - timedelta(1),datetime.now())
# fetch_file_gcs(audio_history[13]['file_url'])

# path='/Users/rishabhindoria/Documents/GitHub/AudioJournaling/airflow/dags/bucketdata1001_DFA_ANG_XX.wav'
# print(get_similar_audios(path))
