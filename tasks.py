from celery import Celery
import redis
import os
from magick_dithering import dither as md_dither
from time import sleep

from google.cloud import storage
    
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost')
CELERY_RESULT_URL = os.environ.get('CELERY_RESULT_URL', 'redis://localhost')

BUCKET_NAME = os.environ.get('GC_BUCKET')

class TaskFailure(Exception):
   pass

celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_URL)

@celery_app.task
def dither(filename, source_dir, dest_dir):
    # try:
        # mock_dither(filename, source_dir, dest_dir)
    md_dither(filename, source_dir, dest_dir)

    upload_blob(f'{dest_dir}/{filename}', filename)

    # except Exception as e:
        # raise TaskFailure('Error during magick dithering').with_traceback(e.__traceback__)

def mock_dither(f, s, d):
    sleep(2)
    if f == 'err':
        raise Exception('mock exception')
    
def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
