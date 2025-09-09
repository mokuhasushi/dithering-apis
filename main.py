from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import shutil

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title='Dithering love APIs')

@app.post('/upload/single')
async def upload_single_file(file: UploadFile = File(...)):
    '''Upload a single file with basic validation'''
    if file.filename == '':
        raise HTTPException(status_code=400, detail='no file selected')
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        'filename': file.filename,
        'content_type': file.content_type,
        'size': file.size,
        'location': str(file_path)
    }


@app.get('/')
async def root():
    return {'message': 'Dithering APIs: upload image at /upload/single'}

