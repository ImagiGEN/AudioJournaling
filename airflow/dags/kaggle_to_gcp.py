import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kaggle.api.kaggle_api_extended import KaggleApi
import google.cloud.storage as gcs
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'soundjot_audio_bucket')
gcs_project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'soundjot')

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

def fetch_from_kaggle(dataset_name, download_path):
    api = KaggleApi()
    api.authenticate()
    data_name = dataset_name.split(',')
    for dset in data_name:
        print("dataset name")
        print(dset)
        api.dataset_download_files(dset, path=download_path, unzip=True)
    print("Data fetched from Kaggle.")

def upload_to_gcs(source_file_path):
    paths = traverse_directory(source_file_path)
    try:
        bucket.reload()
        print(f'Bucket {gcs_bucket_name} exists.')
    except:
        print(f'Bucket {gcs_bucket_name} does not exist.')
        bucket.storage_class = "STANDARD"
        storage_client.create_bucket(bucket, location="us-central1")

    for path in paths:
        destination_blob_name = '/'.join(path.split('/')[-2:])
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(path)
    print("Data uploaded to Google Cloud Storage.")

def traverse_directory(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append(file_path)
    return paths

dag = DAG('kaggle_to_gcs', default_args=default_args, schedule_interval=None)

fetch_data_task = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_from_kaggle,
    op_kwargs={
        'dataset_name': os.getenv("KAGGLE_DATASET_NAME"),
        'download_path': os.getenv("DOWNLOAD_PATH"),
    },
    dag=dag,
)

upload_to_gcs_task = PythonOperator(
    task_id='upload_to_gcs_task',
    python_callable=upload_to_gcs,
    op_kwargs={
        'source_file_path': os.getenv("SOURCE_FILE_PATH"),
    },
    dag=dag,
)

fetch_data_task >> upload_to_gcs_task
