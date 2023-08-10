from sqlalchemy.orm import Session
from utils.db_utils import models, schemas
from utils import generic

def create_user(db: Session, user: schemas.UserCreate):
    if user.cnf_password != user.password:
        raise Exception("Passwords do not match!")
    db_user = models.User(username=user.username,
                          first_name=user.firstname,
                          last_name=user.lastname,
                          password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, credentials: schemas.UserAuthentication):
    result_user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not result_user: # username doesn't exists
        return
    if result_user.check_password(credentials.password):
        return generate_jwt_token(credentials.username, credentials.password, result_user.id)

def generate_jwt_token(username, password, user_id):
    if not (username and password):
        raise Exception(
            status_code=404, detail=r"Username and password cannot be empty")
    data_to_encode = {
        "username": username,
        "password": generic.get_hashed_password(password).decode('utf-8'),
        "user_id": user_id
    }
    access_token = generic.create_access_token(data_to_encode)
    return access_token

def validate_access_token(db: Session, access_token: str):
    if not access_token:
        return False
    decoded_data = generic.decode_token(access_token)
    generic.compare_time(decoded_data["exp"])
    username = decoded_data["username"]
    hashed_password = decoded_data["password"]
    result_user = db.query(models.User).filter(
            models.User.username == username and
            models.User.hashed_password == hashed_password).first()
    if not result_user:
        return False
    return result_user.first_name + " " + result_user.last_name

def add_audio_metadata(db: Session, audio: schemas.UserAudioMetadata):

    db_audio = models.UserAudioMetadata(file_url=audio.file_url,
                                       user_id=audio.user_id)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio

def get_journal_history(db: Session, user_input: schemas.UserAudioHistory):
    db_audio_history = db.query(models.UserAudioMetadata).filter(user_input.user_id == models.UserAudioMetadata.user_id).all()
    result = [{"id": row.id, "file_url": row.file_url} for row in db_audio_history]
    return result

def set_emotion_user_audio(db: Session, user_input: schemas.UserAudioEmotion):
    result = db.query(models.UserAudioMetadata).filter(
        models.UserAudioMetadata.id == user_input.audio_id).first()
    result.emotion = user_input.emotion
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
    result = db.query(models.UserAudioMetadata).filter(
        models.UserAudioMetadata.user_id == user_input.user_id,
        models.UserAudioMetadata.timestamp.between(user_input.start_date, user_input.end_date)
        ).all()
    
    return_result = dict()
    for r in result:
        return_result[r.emotion] = return_result.get(r.emotion, 0) + 1
    return return_result
