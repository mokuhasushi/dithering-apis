import wand
import os

from wand.image import Image
import wand.image

HOST_IMGS_DIRECTORY = os.environ.get('HOST_IMG_DIRECTORY', '/Users/anto/Code/bg-art')
HOST_SOURCE_IMGS = HOST_IMGS_DIRECTORY + '/source-imgs'
HOST_PROCESSED_IMGS = HOST_IMGS_DIRECTORY + '/processed-imgs'


# TODO: as dither code performs in a with block, img is closed at the end of it. 
#       currently returning a blob string works, and it is the intended behavior
# async def dither_from_filename(filename, source_dir, dest_dir):
#     source_path = f'{source_dir}/{filename}'
#     dest_path = f'{dest_dir}/{filename}'
#     with Image(filename=source_path) as img:
#         i = dither(img)
#         i.save(filename=dest_path)
#     return 

# async def dither_file(file):
#     with Image(file=file) as img:
#         return dither(img)

async def dither_blob(blob):
    with Image(blob=blob) as img:
        return dither(img)

def dither(img: Image):
    with img.clone() as i: 
        scale_x, scale_y = img.size[0]//20, img.size[1]//20
        i.scale(scale_x, scale_y)
        i.scale(img.size[0], img.size[1]) 
        with Image(width=256, height=1,
            #    pseudo='gradient:SaddleBrown-LavenderBlush') as amap:
            pseudo='pattern:gray50') as amap:
            i.remap(amap, method=wand.image.DITHER_METHODS[2])
        return i.make_blob()

