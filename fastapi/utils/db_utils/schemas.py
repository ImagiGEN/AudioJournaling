from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile, File


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    cnf_password: str
    firstname: str
    lastname: str

class UserAuthentication(UserBase):
    password: str

class UserAudioMetadata(BaseModel):
    file_url: str
    user_id: int

class UserAudioDetails(BaseModel):
    audio_id: int
    emotion: str
    transcript: str
    quote: str

class DatasetAudio(BaseModel):
    audio_path: str

class UserAccessToken(BaseModel):
    access_token: str

class UserAudioJournal(BaseModel):
    audio_file: UploadFile = File(...)

class CreateAudioJournal(UserAccessToken):
    audio_file_name: str

class UserAudioHistory(UserAccessToken):
    start_date: datetime
    end_date: datetime

class UserJournalAudio(UserAccessToken):
    file_url: str

class UserJournalByDate(UserAccessToken):
    date: datetime
