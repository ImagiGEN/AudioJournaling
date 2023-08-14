from sqlalchemy.orm import Session
from utils.db_utils import models, schemas
from utils import generic
from fastapi import HTTPException
from datetime import datetime
import os

def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code = 404, detail = r"Username already in use!")
    if user.cnf_password != user.password:
        raise HTTPException(status_code = 404, detail = r"Passwords do not match!")
    db_user = models.User(username=user.username,
                          first_name=user.firstname,
                          last_name=user.lastname,
                          password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return dict(db_user)

def get_user_by_username(db: Session, username):
    result_user = db.query(models.User).filter(models.User.username == username).first()
    return result_user

def authenticate_user(db: Session, credentials: schemas.UserAuthentication):
    result_user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not result_user: # username doesn't exists
        raise HTTPException(status_code = 403, detail = r"Forbidden! Please check your username and password")
    if result_user.check_password(credentials.password):
        return {"auth_token": generate_jwt_token(credentials.username, credentials.password, result_user.id)}
    else:
        raise HTTPException(status_code = 403, detail = r"Forbidden! Please check your username and password")
    
def generate_jwt_token(username, password, user_id):
    if not (username and password):
        raise HTTPException(
            status_code=404, detail=r"Username and password cannot be empty")
    data_to_encode = {
        "username": username,
        "password": generic.get_hashed_password(password).decode('utf-8'),
        "user_id": user_id
    }
    access_token = generic.create_access_token(data_to_encode)
    return access_token

def validate_access_token(db: Session, user_input: schemas.UserAccessToken):
    access_token = user_input.access_token
    if not access_token:
        raise HTTPException("No access token found!")
    decoded_data = generic.decode_token(access_token)
    generic.compare_time(decoded_data["exp"])
    username = decoded_data["username"]
    hashed_password = decoded_data["password"]
    result_user = db.query(models.User).filter(
            models.User.username == username and
            models.User.hashed_password == hashed_password).first()
    if not result_user:
        raise HTTPException("Invalid access token!")
    return {"username": result_user.username,
            "name": result_user.first_name + " " + result_user.last_name
            }

def add_audio_metadata(db: Session, audio: schemas.UserAudioMetadata):
    db_audio = models.UserAudioMetadata(file_url=audio.file_url,
                                       user_id=audio.user_id)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio

def get_journal_history(db: Session, user_input: schemas.UserAudioHistory):
    decoded_info = generic.decode_token(user_input.access_token)
    db_audio_history = db.query(models.UserAudioMetadata).filter(decoded_info.get("user_id") == models.UserAudioMetadata.user_id).all()
    result = [{"id": row.id, "file_url": row.file_url} for row in db_audio_history]
    return result

def set_audio_details(db: Session, user_input: schemas.UserAudioDetails):
    result = db.query(models.UserAudioMetadata).filter(
        models.UserAudioMetadata.id == user_input.audio_id).first()
    result.emotion = user_input.emotion
    result.transcript = user_input.transcript
    result.quote = user_input.quote
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_emotion_audio_data(db: Session, user_input: schemas.DatasetAudio):
    result = db.query(models.AudioDataMetadata).filter(models.AudioDataMetadata.path == user_input.audio_path).first()
    if not result:
        raise Exception("Dataset audio not found")
    return result.emotion

def get_user_emotions(db: Session, user_input: schemas.UserAudioHistory):
    decoded_info = generic.decode_token(user_input.access_token)
    result = db.query(models.UserAudioMetadata).filter(
        models.UserAudioMetadata.user_id == decoded_info.get("user_id"),
        models.UserAudioMetadata.timestamp.between(user_input.start_date, user_input.end_date)
        ).all()
    
    return_result = dict()
    for r in result:
        return_result[r.emotion] = return_result.get(r.emotion, 0) + 1
    return return_result

def get_journal_transcript_by_date(db: Session, user_input):
    decoded_info = generic.decode_token(user_input.access_token)
    selected_date = datetime.date(user_input.date)
    s_date = datetime.combine(selected_date, datetime.min.time())
    e_date = datetime.combine(selected_date, datetime.max.time())
    print(s_date, e_date)
    result = db.query(models.UserAudioMetadata).filter(
        models.UserAudioMetadata.user_id == decoded_info.get("user_id"),
        models.UserAudioMetadata.timestamp.between(s_date, e_date)
        ).all()
    return_result = []
    for r in result:
        return_result.append(r.transcript)
    return "\n".join(return_result)
