import os
import google.cloud.storage as gcs
import soundfile as sf
import io


gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME', 'damg7245-summer23-team2-audiojournaling')
gcs_project_id = os.environ.get('GCS_PROJECT_ID', 'damg-soundjot')


storage_client = gcs.Client(project=gcs_project_id)
bucket = storage_client.bucket(gcs_bucket_name)

def initialize_bucket():
    try:
        bucket.reload()
        print(f'Bucket {gcs_bucket_name} exists.')
    except:
        print(f'Bucket {gcs_bucket_name} does not exist.')
        bucket.storage_class = "STANDARD"
        storage_client.create_bucket(bucket, location="us-east1")

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    initialize_bucket()
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def download_sound_blob(source_file_name):
    # read a blob
    blob = bucket.blob(source_file_name)
    file_as_string = blob.download_as_string()

    # convert the string to bytes and then finally to audio samples as floats 
    # and the audio sample rate
    data, sample_rate = sf.read(io.BytesIO(file_as_string))
    return data, sample_rate
