from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Fetch values from environment variables
kaggle_api_key = os.getenv("KAGGLE_API_KEY")
google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
dataset_name = os.getenv("KAGGLE_DATASET_NAME")
gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
download_path = os.getenv("DOWNLOAD_PATH")
source_file_path = os.getenv("SOURCE_FILE_PATH")

def authenticate_kaggle():
    api = KaggleApi()
    api.authenticate()
    return api

def authenticate_gcs(credentials_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return storage.Client()

def fetch_from_kaggle(api, dataset_name, download_path):
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)

def upload_to_gcs(client, bucket_name, source_file_path, destination_blob_name):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

def traverse_directory(path):
    paths=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append(file_path)
    return paths  # You can perform actions on the file_path here


# destination_blob_name = os.getenv("DESTINATION_BLOB_NAME")



# ... (rest of the functions remain the same)


paths=traverse_directory(source_file_path)
# Authenticate and set up connections
kaggle_api = authenticate_kaggle()
gcs_client = authenticate_gcs(google_credentials_path)

# Fetch data from Kaggle
for dset in dataset_name:
    fetch_from_kaggle(kaggle_api, dset, download_path)

# Upload data to Google Cloud Storage
for path in paths:
    destination_blob_name= path.split('/')[-2]+'/'+path.split('/')[-1]
    upload_to_gcs(gcs_client, gcs_bucket_name, path, destination_blob_name)
print("Data uploaded to Google Cloud Storage.")
