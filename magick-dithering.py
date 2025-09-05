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

def compile_command(source_img: str, dest_img: str | None, algorithm: str | None = "", resize: str | None = "", remap: str | None = "", last_cmd: bool = True):
    resize_str = f'-resize {resize}' if resize else ''
    remap_str = f'-remap {remap}' if remap else ''
    return f'{CONTAINER_SOURCE_IMGS}/{source_img} {resize_str} {algorithm} {remap_str} {CONTAINER_PROCESSED_IMGS if last_cmd else CONTAINER_SOURCE_IMGS}/{dest_img}'

test_cmd = compile_command(
    'paris-texas.jpg', 
    'paris-1.jpg',
    algorithm="-dither FloydSteinberg", 
    remap="pattern:gray50"
    )

def make_blocky():
    cmd_1 = compile_command('roman-dmitry.png', '_tmp.png', algorithm='-scale 5%', last_cmd=False)
    cmd_2 = compile_command('_tmp.png', 'blocky3.png', algorithm='-scale 2000% -filter point', remap='pattern:gray50')
    
    client.containers.run(IMAGEMAGICK_CONTAINER,
                      cmd_1,
                      volumes=VOLUME_LIST)
    client.containers.run(IMAGEMAGICK_CONTAINER,
                      cmd_2,
                      volumes=VOLUME_LIST)

make_blocky()
# if __name__ == '__main__' : 
