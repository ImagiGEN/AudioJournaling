from generic import decode_token
from db_utils import crud, schemas
from gcp_utils import bucket
import uuid
import os

def create_new_audio(audio_file_name, access_token):
    decoded_info = decode_token(access_token)
    destination_file_name = os.path.join(str(decoded_info.get("username")), str(audio_file_name), str(uuid.uuid4()))
    bucket.upload_blob(audio_file_name, destination_file_name)
    data = {
        "file_url": destination_file_name,
        "user_id": decoded_info.get("user_id")
        }
    user = schemas.UserAudioMetadata(**data)
    crud.add_audio_metadata()


