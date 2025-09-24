from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import uuid
from datetime import datetime, timezone

from validators import ImageValidator

import os
from magick_dithering import dither_blob

from google.cloud import storage

BUCKET_NAME = os.environ.get('GC_BUCKET')

app = FastAPI(title='Dithering love APIs')

img_validator = ImageValidator(max_size=25 * 1024 * 1024)

@app.post('/upload/single')
async def upload_single_file(file: UploadFile = File(...)):
    '''Upload a single file with validation'''

    validation = await img_validator.validate_file(file)

    if not validation['valid']:
        raise HTTPException(
            status_code=400, 
            detail={
                'message': 'File validation failed',
                'errors': validation['errors']
                })
    
    file_ext = Path(file.filename).suffix
    file_uuid = uuid.uuid4()
    unique_filename = f'{file_uuid}{file_ext}'

    try:
        f = await file.read()
        img_blob = await dither_blob(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Failed to dither image: {str(e)}'
        )

    # upload
    try:
        processed_url = upload_blob_from_string(img_blob, unique_filename)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Failed to upload file: {str(e)}'
        )

    
    return {
        'success': True,
        'original_filename': file.filename,
        'stored_filename': file_uuid,
        'processed_url': processed_url,
        'content_type': file.content_type,
        'size': file.size,
        'upload_time': datetime.now(timezone.utc).isoformat(),
    }


@app.get('/')
async def root():
    return {'message': 'Dithering APIs: upload image at /upload/single'}

def upload_blob_from_file(file):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"uploaded/{file.filename}")

    blob.upload_from_file(file.file)

    print(
        f"File {file.filename} uploaded!"
    )

    return blob.public_url

def upload_blob_from_string(img_blob, filename):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"uploaded/{filename}")

    blob.upload_from_string(img_blob)

    print(
        f"File {filename} uploaded!"
    )

    return blob.public_url

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

    return blob.public_url
