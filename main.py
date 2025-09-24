from fastapi import FastAPI, File, UploadFile, HTTPException
from validators import ImageValidator

from pathlib import Path
import uuid
from datetime import datetime, timezone

from magick_dithering import dither_blob

from cloud_storage import upload_blob_from_string

app = FastAPI(title='Dithering love APIs')

img_validator = ImageValidator(max_size=25 * 1024 * 1024)

@app.post('/dither')
async def upload_single_file(file: UploadFile = File(...)):
    '''Upload a single file with validation'''

    #validate
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

    # dither
    try:
        f = await file.read()
        img_blob = await dither_blob(f)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f'Failed to dither image: {str(e)}'
        )

    # upload
    try:
        processed_url = upload_blob_from_string(img_blob, unique_filename)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f'Failed to upload file: {str(e)}'
        )

    
    return {
        'success': True,
        'original_filename': file.filename,
        'processed_url': processed_url,
        'upload_time': datetime.now(timezone.utc).isoformat(),
    }


@app.get('/')
async def root():
    return {'message': 'Dithering APIs: upload image at /dither'}

