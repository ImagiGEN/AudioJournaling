import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kaggle.api.kaggle_api_extended import KaggleApi
import google.cloud.storage as gcs
from dotenv import load_dotenv
import json

# Load variables from .env file
load_dotenv()
gcs_project_id = os.environ.get('GCS_PROJECT_ID', 'soundjot')

storage_client = gcs.Client(project=gcs_project_id)
print(storage_client)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 6),
    'retries': 1,
}

def authenticate_kaggle():
    api = KaggleApi()
    api.authenticate()
    return api

def authenticate_gcs():
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
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
    return paths

def fetch_and_upload(**kwargs):
    kaggle_api = authenticate_kaggle()
    gcs_client = authenticate_gcs(kwargs['ti'].xcom_pull(task_ids='authenticate_gcs_task'))

    paths = traverse_directory(kwargs['source_file_path'])

    for dset in kwargs['dataset_name']:
        fetch_from_kaggle(kaggle_api, dset, kwargs['download_path'])

    for path in paths:
        destination_blob_name = path.split('/')[-2] + '/' + path.split('/')[-1]
        upload_to_gcs(gcs_client, kwargs['gcs_bucket_name'], path, destination_blob_name)
    print("Data uploaded to Google Cloud Storage.")

dag = DAG('kaggle_to_gcs', default_args=default_args, schedule_interval=None)

authenticate_gcs_task = PythonOperator(
    task_id='authenticate_gcs_task',
    python_callable=authenticate_gcs,
    # op_args=[os.getenv("GOOGLE_CREDENTIALS_PATH")],
    dag=dag,
)

fetch_and_upload_task = PythonOperator(
    task_id='fetch_and_upload_task',
    python_callable=fetch_and_upload,
    op_kwargs={
        'dataset_name': os.getenv("KAGGLE_DATASET_NAME"),
        'download_path': os.getenv("DOWNLOAD_PATH"),
        'gcs_bucket_name': os.getenv("GCS_BUCKET_NAME"),
        'source_file_path': os.getenv("SOURCE_FILE_PATH"),
    },
    provide_context=True,
    dag=dag,
)

authenticate_gcs_task >> fetch_and_upload_task
