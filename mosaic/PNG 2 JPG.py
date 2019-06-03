from PIL import Image
import os, sys

target_dir = 'F:\\png2jpg'



files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

for filename in files:
    if os.path.splitext(filename)[1] == '.png':
        im = Image.open(os.path.join(target_dir, filename))
        im.convert('RGB').save(os.path.join(target_dir, os.path.splitext(filename)[0] + '.jpg'), 'JPEG')

