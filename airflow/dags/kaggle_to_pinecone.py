import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import google.cloud.storage as gcs
import pinecone
from panns_inference import AudioTagging
from dotenv import load_dotenv
from utils.db_utils import engine
from airflow.models.baseoperator import chain
from kaggle.api.kaggle_api_extended import KaggleApi
import librosa


# Load variables from .env file
load_dotenv()

gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'damg7245-summer23-team2-dataset')
gcs_project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'damg-soundjot')
pinecone_index = os.getenv('PINECONE_INDEX', 'audio-embeddings')
pinecone_api_key = os.getenv('PINECONE_API_KEY', "d28abaee-e61a-4eef-9d3b-2d26cbf3376b")
pinecone_environment = os.getenv('PINECONE_ENVIRONMENT', 'asia-southeast1-gcp-free')
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

def fetch_metadata():
    with engine.connect() as con:
        rs = con.execute('SELECT * FROM audio_data_metadata')
    result = [row for row in rs]
    return result

def fetch_from_kaggle(dataset_name, download_path):
    api = KaggleApi()
    api.authenticate()
    data_name = dataset_name.split(',')
    for dset in data_name:
        print("dataset name")
        print(dset)
        api.dataset_download_files(dset, path=download_path, unzip=True)
    print("Data fetched from Kaggle.")

def initialize_pinecone():
    # Initialize Pinecone client
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_environment
    )

    if pinecone_index not in pinecone.list_indexes():
        pinecone.create_index(
            pinecone_index,
            dimension=2048,
            metric="cosine"
        )

def compute_embeddings():
    initialize_pinecone()
    audio_tagging = AudioTagging(checkpoint_path=None, device='cuda')
    data_metadata = fetch_metadata()
    
    index = pinecone.Index(pinecone_index)

    for row in data_metadata:
        if not row.path:
            continue
        y, _ = librosa.load(row.path, mono=True, sr=None)
        print(f"Generating Embedding for: {row.path}")
        _, emb = audio_tagging.inference(y[None, :])
        to_upsert = list([(str(row.path), emb.tolist())])
        _ = index.upsert(vectors=to_upsert)


# Create the DAG
dag = DAG('kaggle_to_pinecone', default_args=default_args, schedule_interval=None)

# Define the task
fetch_data_kaggle_task = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_from_kaggle,
    op_kwargs={
        'dataset_name': os.getenv("KAGGLE_DATASET_NAME"),
        'download_path': os.getenv("DATA_DOWNLOAD_PATH"),
    },
    dag=dag,
)

compute_embeddings_task = PythonOperator(
    task_id='compute_embeddings',
    python_callable=compute_embeddings,
    provide_context=True,
    dag=dag,
)

# Set task dependencies (there are no downstream tasks in this example)
chain(fetch_data_kaggle_task, compute_embeddings_task)
