from sqlalchemy.orm import Session
import os
from utils.generic import decode_token, get_audio_transcript, llm
from utils.gcp_utils import bucket
from utils.db_utils import schemas, crud
from utils.pinecone_utils import get_similar_audios
import uuid
import speech_recognition as sr

def create_audio_journal_entry(db: Session, user_input: schemas.CreateAudioJournal):
    decoded_info = decode_token(user_input.access_token)
    destination_file_name = os.path.join(str(decoded_info.get("user_id")), str(uuid.uuid4()), user_input.audio_file_name.split("/")[-1])
    bucket.upload_blob(user_input.audio_file_name, destination_file_name)
    
    data = {
        "file_url": destination_file_name,
        "user_id": decoded_info.get("user_id")
        }
    audio = schemas.UserAudioMetadata(**data)
    db_audio = crud.add_audio_metadata(db, audio)
    transcript, emotion = process_user_audio(db, destination_file_name)
    data = {
        "audio_id": db_audio.id,
        "emotion": emotion
    }
    user_input = schemas.UserAudioEmotion(**data)
    crud.set_emotion_user_audio(db, user_input)
    return {"quote": llm.generate_suggestions(transcript, emotion)}

def process_user_audio(db: Session, file_url):
    local_file_name = bucket.download_as_file(file_url)
    transcript = get_audio_transcript(local_file_name)
    audio_ids = get_similar_audios(local_file_name)
    data = {
        "audio_path": audio_ids[0] 
    }
    user_input = schemas.DatasetAudio(**data)
    emotion = crud.get_emotion_audio_data(db, user_input)
    return transcript, emotion
