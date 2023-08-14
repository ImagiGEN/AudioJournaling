from sqlalchemy.orm import Session
import os
from utils.generic import decode_token, get_audio_transcript, llm
from utils.gcp_utils import bucket
from utils.db_utils import schemas, crud
from utils.pinecone_utils import get_similar_audios
import uuid
import speech_recognition as sr
from datetime import datetime

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
    quote = llm.generate_suggestions(transcript, emotion)
    data = {
        "audio_id": db_audio.id,
        "emotion": emotion,
        "transcript": transcript,
        "quote": quote
    }
    user_input = schemas.UserAudioDetails(**data)
    crud.set_audio_details(db, user_input)
    return {"quote": quote, "emotion": emotion}

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

def get_journal_by_date(db: Session, user_input: schemas.UserJournalByDate):
    results = crud.get_journal_transcript_by_date(db, user_input)
    summary = llm.generate_summary(results)
    return_results = {
        "transcript": results,
        "summary": summary,
        "date" : user_input.date.isoformat()
    }
    return return_results

