import docker
import os 

HOST_IMGS_DIRECTORY = os.environ.get('HOST_IMG_DIRECTORY', '/Users/anto/Code/bg-art')
HOST_SOURCE_IMGS = HOST_IMGS_DIRECTORY + '/source-imgs'
HOST_PROCESSED_IMGS = HOST_IMGS_DIRECTORY + '/processed-imgs'
CONTAINER_SOURCE_IMGS = '/source-imgs'
CONTAINER_PROCESSED_IMGS = '/processed-imgs'

IMAGEMAGICK_CONTAINER = 'dpokidov/imagemagick'

VOLUME_LIST = [f'{HOST_SOURCE_IMGS}:{CONTAINER_SOURCE_IMGS}', f'{HOST_PROCESSED_IMGS}:{CONTAINER_PROCESSED_IMGS}']

client = docker.from_env()

def compile_command(source_img: str, dest_img: str | None, algorithm: str, resize: str | None="", remap:str | None=""):
    return f'{source_img} {resize} {algorithm} {remap} {dest_img}'

test_cmd = compile_command(
    CONTAINER_SOURCE_IMGS+'/paris-texas.jpg', 
    CONTAINER_PROCESSED_IMGS+'/paris-1.jpg',
    algorithm="-dither FloydSteinberg", 
    remap="-remap pattern:gray50"
    )
    
client.containers.run(IMAGEMAGICK_CONTAINER,
                      test_cmd,
                      volumes=VOLUME_LIST)

# if __name__ == '__main__' : 
