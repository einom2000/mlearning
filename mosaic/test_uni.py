import piexif

exif_dict = piexif.load("test_uni.jpg")
# thumbnail = exif_dict.pop("thumbnail")
# print(thumbnail)
# if thumbnail is not None:
#     with open("thumbnail.jpg", "wb+") as f:
#         f.write(thumbnail)
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
exif_dict['0th'][33432] = b'abcdefghijklmn'
print(exif_dict)
exif_byte = piexif.dump(exif_dict)
piexif.insert(exif_byte, 'test_uni.jpg')
