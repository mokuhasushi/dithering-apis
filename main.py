from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
from datetime import datetime, timezone

from validators import ImageValidator

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

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
    unique_filename = f'{uuid.uuid4()}{file_ext}'
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Failed to save file: {str(e)}'
        )
    
    return {
        'success': True,
        'original_filename': file.filename,
        'stored_filename': unique_filename,
        'content_type': file.content_type,
        'size': file.size,
        'upload_time': datetime.now(timezone.utc).isoformat(),
    }


@app.get('/')
async def root():
    return {'message': 'Dithering APIs: upload image at /upload/single'}

