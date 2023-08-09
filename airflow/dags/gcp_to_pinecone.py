import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import google.cloud.storage as gcs
import pinecone
from panns_inference import AudioTagging
from dotenv import load_dotenv
# import librosa
import numpy as np
from tqdm.auto import tqdm

# Load variables from .env file
load_dotenv()

gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'soundjot_audio_bucket')
gcs_project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'soundjot')
GOOGLE_APPLICATION_CREDENTIALS = '/Users/rishabhindoria/Documents/GitHub/AudioJournaling/airflow/keys/application_default_credentials.json'

# Initialize Google Cloud Storage client
storage_client = gcs.Client(project=gcs_project_id)
bucket = storage_client.bucket(gcs_bucket_name)

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 7),
    'retries': 1,
}

def fetch_from_gcs_and_process(**kwargs):
    import librosa
    # Fetch audio files from GCS bucket
    source_files = bucket.list_blobs()
    local_directory = 'bucketdata'

    # Iterate through blobs and download each file
    for blob in source_files:
        local_file_path = local_directory + blob.name
        blob.download_to_filename(local_file_path)

    afs = []
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)

    for file_name in files_in_directory:
        if file_name.startswith("bucketdata"):
            afs.append(file_name)

    # Initialize Pinecone client
    pinecone_index = os.getenv('PINECONE_INDEX', 'audio-embeddings')
    pinecone.init(
        api_key="52a077fc-5c01-4cd5-8501-ddb300e9e5bf",
        environment="asia-southeast1-gcp-free"
    )

    if pinecone_index not in pinecone.list_indexes():
        pinecone.create_index(
            pinecone_index,
            dimension=2048,
            metric="cosine"
        )

    index = pinecone.Index(pinecone_index)

    audio_tagging = AudioTagging(checkpoint_path=None, device='cuda')

    audios = []
    _, sr = librosa.load(afs[0])
    for af in afs:
        y, _ = librosa.load(af, mono=True, sr=None)
        audios.append(np.float64(y))

    audios = [np.array(a) for a in audios]
    audios = np.array(audios)
    batch_size = 1

    for i in tqdm(range(0, len(audios), batch_size)):
        batch = audios[i]
        _, emb = audio_tagging.inference(batch[None, :])
        to_upsert = list([(str(i), emb.tolist())])
        _ = index.upsert(vectors=to_upsert)

    index.describe_index_stats()
    print("Data processed and embeddings stored in Pinecone.")

# Create the DAG
dag = DAG('gcs_to_pinecone', default_args=default_args, schedule_interval=None)

# Define the task
fetch_and_process_task = PythonOperator(
    task_id='fetch_and_process_task',
    python_callable=fetch_from_gcs_and_process,
    provide_context=True,
    dag=dag,
)

# Set task dependencies (there are no downstream tasks in this example)
fetch_and_process_task