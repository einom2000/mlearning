from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime



def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


data = get_exif('test_c.jpg')

# all info
for key in data.keys():
    print(str(key) + ":" + str(data[key]))

print()
print()

# 3 time stamps
time_keys = ['DateTimeOriginal',
             'DateTimeDigitized',
             'DateTime']
for key in time_keys:
    d = datetime.strptime(data[key], "%Y:%m:%d %H:%M:%S")
    print(str(key) + ': ', end='')
    print(d)

# original size
exif_sizes = ['ExifImageWidth', 'ExifImageHeight']
s = (int(data[exif_sizes[0]]), int(data[exif_sizes[1]]))
print('image original size: ', end='')
print(s)

gpsinfo = {}
for key in data['GPSInfo'].keys():
    decode = GPSTAGS.get(key, key)
    gpsinfo[decode] = data['GPSInfo'][key]
print(gpsinfo)

