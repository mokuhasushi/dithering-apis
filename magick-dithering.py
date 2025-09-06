import wand
import os

from wand.image import Image
import wand.image

HOST_IMGS_DIRECTORY = os.environ.get('HOST_IMG_DIRECTORY', '/Users/anto/Code/bg-art')
HOST_SOURCE_IMGS = HOST_IMGS_DIRECTORY + '/source-imgs'
HOST_PROCESSED_IMGS = HOST_IMGS_DIRECTORY + '/processed-imgs'



# def compile_command(source_img: str, dest_img: str | None, algorithm: str | None = "", resize: str | None = "", remap: str | None = "", last_cmd: bool = True):
#     resize_str = f'-resize {resize}' if resize else ''
#     remap_str = f'-remap {remap}' if remap else ''
#     return f'{source_img} {resize_str} {algorithm} {remap_str} {dest_img}'

# test_cmd = compile_command(
#     'paris-texas.jpg', 
#     'paris-1.jpg',
#     algorithm="-dither FloydSteinberg", 
#     remap="pattern:gray50"
#     )



# def make_blocky():
#     cmd_1 = compile_command('roman-dmitry.png', '_tmp.png', algorithm='-scale 5%', last_cmd=False)
#     cmd_2 = compile_command('_tmp.png', 'blocky3.png', algorithm='-scale 2000% -filter point', remap='pattern:gray50')
    
with Image(filename='source-imgs/eagle.png') as img:
    with img.clone() as i: 
        scale_x, scale_y = img.size[0]//20, img.size[1]//20
        i.scale(scale_x, scale_y)
        i.scale(img.size[0], img.size[1]) 
        with Image(width=256, height=1,
            #    pseudo='gradient:SaddleBrown-LavenderBlush') as amap:
               pseudo='pattern:gray50') as amap:
            i.remap(amap, method=wand.image.DITHER_METHODS[2])
        i.save(filename='./processed-imgs/blocky4.png')


# if __name__ == '__main__' : 
