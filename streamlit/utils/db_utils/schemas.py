from pydantic import BaseModel


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
