from pydub import AudioSegment
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def get_emotion(audio_file_wav):
    try:
        audio = AudioSegment.from_wav(audio_file_wav)
        file_name = audio_file_wav.replace(".wav", ".flac")
        audio.export(file_name,format = "flac")
        def query(filename):
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            return response.json()
        output = query(file_name)
        if output:
            return output[0].get("label")
    except Exception as e:
        print({str(e)})
        return None
