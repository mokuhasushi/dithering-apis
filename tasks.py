from celery import Celery
import redis
# from magick_dithering import dither
from time import sleep

class TaskFailure(Exception):
   pass

celery_app = Celery('tasks', broker='redis://localhost', backend='redis://localhost')

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