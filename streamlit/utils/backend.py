from utils.db_utils import SessionLocal, crud, schemas, models, engine
from utils.generic import decode_token
from utils.gcp_utils import bucket
import os
import uuid

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
    destination_file_name = os.path.join(str(decoded_info.get("user_id")), str(uuid.uuid4()))
    bucket.upload_blob(audio_file_name, destination_file_name)
    data = {
        "file_url": destination_file_name,
        "user_id": decoded_info.get("user_id")
        }
    audio = schemas.UserAudioMetadata(**data)
    crud.add_audio_metadata(db, audio)

# create_user("ashritha@gmail.com", "ashritha", "ashritha", "ashritha", "ashritha")
# jwt_token = authenticate_user("ashritha@gmail.com", "ashritha")
# print(validate_access_token(jwt_token))
# create_new_audio("/Users/sayalidalvi/ashritha/Project_old/audio_journaling/archive/Actor_01/03-01-04-02-01-01-01.wav", jwt_token)
