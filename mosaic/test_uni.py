import piexif
import datetime
exif_dict = piexif.load("test_uni.jpg")
# thumbnail = exif_dict.pop("thumbnail")
# print(thumbnail)
# if thumbnail is not None:
#     with open("thumbnail.jpg", "wb+") as f:
#         f.write(thumbnail)

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

exif_ifd = {piexif.ExifIFD.DateTimeOriginal: t,
            piexif.ExifIFD.LensMake: u"ManualSet",
            piexif.ExifIFD.Sharpness: 65535,
            piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
            }
exif_dict["Exif"] = exif_ifd
exif_dict['0th'][270] = b'this is a test'
exif_dict['0th'][33432] = b'this is a test too'
print(exif_dict)
exif_byte = piexif.dump(exif_dict)
piexif.insert(exif_byte, 'test_uni.jpg')
