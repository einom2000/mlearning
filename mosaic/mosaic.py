import PIL
from PIL import Image
from PIL import ImageFilter
import math


def get_average_color(x, y):
    R, G, B = 0, 0, 0
    for pixel_x in range(tiles_x):
        for pixel_y in range(tiles_y):
            r, g, b = img.getpixel((x * tiles_x + pixel_x , y * tiles_y + pixel_y))
            R += r
            G += g
            B += b
    return R // pixels_per_tile, G // pixels_per_tile, B // pixels_per_tile


def mosaic_zone(x, y):

    for pixel_x in range(tiles_x):
        for pixel_y in range(tiles_y):
            img.putpixel((x * tiles_x + pixel_x , y * tiles_y + pixel_y), (avr_r, avr_g, avr_b))

ratio = 0.06

def mosaic(file, ratio):
    global tiles_vertical, tiles_horizontal, tiles_x, tiles_y
    global avr_r, avr_g, avr_b
    global pixels_per_tile, img

    img = Image.open(file)

    tiles_horizontal = int(img.size[0] / (ratio * 0.1 * img.size[0]))
    tiles_vertical = int(img.size[1] / (ratio * 0.1 * img.size[1]))


    if tiles_horizontal > img.size[0]:
        tiles_horizontal = img.size[0]
    if tiles_vertical > img.size[1]:
        tiles_vertical = img.size[1]

    x = math.floor(img.size[0] / tiles_horizontal) * tiles_horizontal
    y = math.floor(img.size[1] / tiles_vertical) * tiles_vertical
    img = img.resize((x, y), PIL.Image.ANTIALIAS)

    tiles_x = img.size[0] // tiles_horizontal
    tiles_y = img.size[1] // tiles_vertical
    pixels_per_tile = tiles_x * tiles_y


    for x in range(tiles_horizontal):
        for y in range(tiles_vertical):
            avr_r, avr_g, avr_b = (get_average_color(x, y))
            mosaic_zone(x, y)
    img.show()


if __name__ == "__main__":
    mosaic('test_c.jpg', 2)
