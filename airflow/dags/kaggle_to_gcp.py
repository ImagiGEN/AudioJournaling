import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kaggle.api.kaggle_api_extended import KaggleApi
import google.cloud.storage as gcs
from dotenv import load_dotenv
from utils.db_utils import engine
from sqlalchemy import text
# Load variables from .env file
load_dotenv()

gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'damg7245-summer23-team2-dataset')
gcs_project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'damg-soundjot')

storage_client = gcs.Client(project=gcs_project_id)
bucket = storage_client.bucket(gcs_bucket_name)
kaggle_api = KaggleApi()
kaggle_api.authenticate()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 6),
    'retries': 1,
}

def fetch_metadata():
    with engine.connect() as con:
        rs = con.execute(text('select * from audio_data_metadata'))
    result = [row for row in rs]
    return result

def initialize_bucket():
    try:
        bucket.reload()
        print(f'Bucket {gcs_bucket_name} exists.')
    except:
        print(f'Bucket {gcs_bucket_name} does not exist.')
        bucket.storage_class = "STANDARD"
        storage_client.create_bucket(bucket, location="us-east1")

def fetch_from_kaggle(dataset_name, download_path):
    api = KaggleApi()
    api.authenticate()
    data_name = dataset_name.split(',')
    for dset in data_name:
        print("dataset name")
        print(dset)
        api.dataset_download_files(dset, path=download_path, unzip=True)
    print("Data fetched from Kaggle.")

def upload_to_gcs():
    initialize_bucket()
    data_df = fetch_metadata()
    for row in data_df:
        print(f"Uploading file: {row.path}")
        blob = bucket.blob(row.path[1:])
        blob.upload_from_filename(row.path)
    print("Data uploaded to Google Cloud Storage.")

dag = DAG('kaggle_to_gcs', default_args=default_args, schedule_interval=None)

fetch_data_task = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_from_kaggle,
    op_kwargs={
        'dataset_name': os.getenv("KAGGLE_DATASET_NAME"),
        'download_path': os.getenv("DATA_DOWNLOAD_PATH"),
    },
    dag=dag,
)

upload_to_gcs_task = PythonOperator(
    task_id='upload_to_gcs_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        'source_file_path': os.getenv("DATA_DOWNLOAD_PATH"),
    },
    dag=dag,
)

fetch_data_task >> upload_to_gcs_task
