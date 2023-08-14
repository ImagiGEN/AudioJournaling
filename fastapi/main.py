from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from utils.db_utils import models, schemas, engine, SessionLocal, crud
from utils.generic import decode_token, journal
from utils.gcp_utils import bucket
from sqlalchemy.orm import Session
import os
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoundJot")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/health")
async def check() -> dict:
    return {"message": "OK"}

@app.post("/api/v1/user")
async def register_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):
    if not (user_input.username and
            user_input.password and
            user_input.cnf_password and
            user_input.firstname and
            user_input.lastname):
        raise HTTPException(
            status_code=404, detail=r"Username and password cannot be empty")
    if user_input.password != user_input.cnf_password:
        raise HTTPException(
            status_code=404, detail=r"Provided passwords do not match")
    try:
        result = crud.create_user(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)


@app.post("/api/v1/user/authenticate")
async def authenticate_user(user_input: schemas.UserAuthentication, db: Session = Depends(get_db)):
    try:
        result = crud.authenticate_user(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@app.get("/api/v1/user/access_token")
async def validate_access_token(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        result = crud.validate_access_token(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@app.post("/api/v1/user/journal/create")
async def create_journal_entry(access_token: str = Form(...), audio_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_folder = f"files/{str(uuid.uuid4())}"
        os.makedirs(file_folder, exist_ok=True)

        file_location = os.path.join(file_folder, audio_file.filename.split('/')[-1])
        with open(file_location, "wb+") as file_object:
            file_object.write(audio_file.file.read())
        journal_input = {
            "access_token": access_token,
            "audio_file_name": file_location
        }
        journal_input = schemas.CreateAudioJournal(**journal_input)
        result = journal.create_audio_journal_entry(db, journal_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@app.get("/api/v1/user/journal/history")
async def fetch_journal_history(user_input: schemas.UserAudioHistory, db: Session = Depends(get_db)):
    try:
        result = crud.get_journal_history(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@app.get("/api/v1/user/journal/audio")
async def fetch_audio_file(user_input: schemas.UserJournalAudio, db: Session = Depends(get_db)):
    downloaded_file = bucket.download_as_file(user_input.file_url)
    return FileResponse(downloaded_file, media_type="audio/wav", headers={"Content-Disposition": "attachment; filename=audio.wav"})

@app.get("/api/v1/user/emotion/history")
async def get_user_emotion_history(user_input: schemas.UserAudioHistory, db: Session = Depends(get_db)):
    try:
        result = crud.validate_access_token(db, user_input)
        result = crud.get_user_emotions(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@app.get("/api/v1/user/journal/transcript")
async def get_journal_transcript(user_input: schemas.UserJournalByDate, db: Session = Depends(get_db)):
    try:
        result = journal.get_journal_by_date(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)
