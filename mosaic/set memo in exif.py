import piexif
import datetime
import os


dic = {
        'Title': b'',
        'Author': b'',
        'CopyRight': b''
       }

tar_dir = 'F:\\test'


for dirpath, dirnames, filenames in os.walk(tar_dir):
    for filename in filenames:
        if os.path.splitext(filename)[1][1:] == 'jpg':
            full_path = os.p
            exif_dict = piexif.load("test_uni.jpg")

print(exif_dict)
for ifd_name in exif_dict:
    print('=======================================')
    print("\n{0} IFD:".format(ifd_name))
    if exif_dict[ifd_name] is not None and exif_dict[ifd_name] != {}:
        for key in exif_dict[ifd_name]:
            print(str(key) + ': ', end='')
            print(exif_dict[ifd_name][key])
    else:
        print('None')
t = datetime.datetime.strftime(datetime.datetime.now(), "%Y:%m:%d %H:%M:%S")
print(t)

exif_dict['0th'][270] = b'this is a test'
exif_dict['0th'][33432] = b'this is a test too'
exif_dict['0th'][315] = b' there is another place'
print(exif_dict)
exif_byte = piexif.dump(exif_dict)
piexif.insert(exif_byte, 'test_uni.jpg')
