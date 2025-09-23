from fastapi import FastAPI, File, UploadFile, HTTPException
from redis import Redis
from pathlib import Path
import shutil
import uuid
from datetime import datetime, timezone

from validators import ImageValidator
from tasks import dither, celery_app
from celery.result import AsyncResult

import os

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

PROCESSED_DIR = Path('processed')
PROCESSED_DIR.mkdir(exist_ok=True)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_USERNAME = os.environ.get('REDIS_USERNAME', None)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

app = FastAPI(title='Dithering love APIs')

r = Redis(host=REDIS_HOST, port=6379, decode_responses=True)
r = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
)

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
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Failed to save file: {str(e)}'
        )
    
    result = dither.delay(unique_filename, str(UPLOAD_DIR), str(PROCESSED_DIR))
    r.set(str(file_uuid), result.id)
    
    return {
        'success': True,
        'original_filename': file.filename,
        'stored_filename': file_uuid,
        'content_type': file.content_type,
        'size': file.size,
        'upload_time': datetime.now(timezone.utc).isoformat(),
    }

@app.get('/status/{filename}')
async def check_status(filename: str):
    uuid = r.get(filename)
    if not uuid:
        return HTTPException(
            status_code=404,
            detail={'message': 'No task associated with this filename'}
        )
    
    res = AsyncResult(uuid, app=celery_app)
    state = res.status
    return {'task_status': state}

@app.get('/')
async def root():
    return {'message': 'Dithering APIs: upload image at /upload/single'}

