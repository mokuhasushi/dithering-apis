from celery import Celery
import redis
import os
# from magick_dithering import dither
from time import sleep

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost')
CELERY_RESULT_URL = os.environ.get('CELERY_RESULT_URL', 'redis://localhost')

class TaskFailure(Exception):
   pass

celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_URL)

@celery_app.task
def dither(filename, source_dir, dest_dir):
    try:
        mock_dither(filename, source_dir, dest_dir)
        # dither(filename, source_dir, dest_dir)
    except Exception as e:
        raise TaskFailure('Error during magick dithering').with_traceback(e.__traceback__)

def mock_dither(f, s, d):
    sleep(2)
    if f == 'err':
        raise Exception('mock exception')