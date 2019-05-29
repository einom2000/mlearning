import piexif
from PIL import Image
from PIL.ExifTags import TAGS


fn = "test_uni.jpg"


def test_PIL():
    # test PIL
    print('\n<< Test of PIL >> \n' )
    img = Image.open(fn)
    info = img._getexif()
    for k, v in info.items():
        nice = TAGS.get(k, k)
        print( '%s (%s) = %s' % (nice, k, v) )

test_PIL()

print('======================================')
from iptcinfo3 import IPTCInfo



info = IPTCInfo(fn)
print(info['keywords'])
print(info['object name'])

print(info.data())
