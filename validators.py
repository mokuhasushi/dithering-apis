from pathlib import Path
from fastapi import UploadFile

class ImageValidator:
    def __init__(self, max_size=10*1024*1024):
        self.max_size = max_size
        self.allowed_extensions = {'.png', '.jpg', '.webp', '.gif', '.txt'}
    
    async def validate_file(self, file:UploadFile) -> dict:
        '''Check if the file is valid'''
        result = {'valid': False, 'errors':[]}

        if not file.filename or file.filename.strip == '':
            result['errors'].append('No file selected')
            return result
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            result['errors'].append(f'File extensions {file_ext} not allowed')
            return result
        
        content = await file.read()
        await file.seek(0)

        file_size = len(content)
        if file_size > self.max_size:
            result['errors'].append(f'File size too large ({file_size:,} bytes). Maximum: {self.max_size:,} bytes')

        result['valid'] = True 
        return result