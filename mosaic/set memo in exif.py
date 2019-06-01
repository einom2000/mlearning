import piexif
import datetime
import os
import time

dic = {
        'Title': b'Familey Memo',
        'Author': b'Exifed, dedupilcated, backuped',
        'CopyRight': 'singled and backuped on '
       }

# tar_dir = 'E:\\已经备备_以后又增加_整理，更名，全EXIF相册，唯一'
tar_dir = 'E:\\test'

count = 1
max_count = sum([len(files) for r, d, files in os.walk(tar_dir)])

for dirpath, dirnames, filenames in os.walk(tar_dir):
    for filename in filenames:
        print('Handling %d in total %d files.', (count, max_count))
        count += 1
        if os.path.splitext(filename)[1][1:].lower() == 'jpg'\
                or os.path.splitext(filename)[1][1:].lower() == 'jpeg':
            full_path = os.path.join(dirpath, filename)
            # print(full_path)
            exif_dict = piexif.load(full_path)

            # print(exif_dict)
            if os.stat(full_path).st_mode == 33060:
                os.chmod(full_path, 33206)
            # print(os.stat(full_path).st_mode)
            for ifd_name in exif_dict:
                # print('=======================================')
                # print("\n{0} IFD:".format(ifd_name))
                if exif_dict[ifd_name] is not None and exif_dict[ifd_name] != {}:
                    for key in exif_dict[ifd_name]:
                        # print(str(key) + ': ', end='')
                        # print(exif_dict[ifd_name][key])
                        pass
                else:
                    print('None')
            print(full_path)
            print(exif_dict)
            if '0th' not in exif_dict.keys():
                exif_dict['0th'] = {}
            if 270 not in exif_dict['0th'].keys():
                exif_dict['0th'][270] = b''
            if 315 not in exif_dict['0th'].keys():
                exif_dict['0th'][315] = b''
            if 33432 not in exif_dict['0th'].keys():
                exif_dict['0th'][33432] = b''

            if exif_dict['0th'][270] != dic['Title']:
                today = datetime.datetime.strftime(datetime.datetime.now(), "%Y:%m:%d %H:%M:%S")
                exif_dict['0th'][270] = dic['Title']
                exif_dict['0th'][315] = dic['Author']
                exif_dict['0th'][33432] = str.encode(dic['CopyRight'] + today)
                exif_byte = piexif.dump(exif_dict)
                piexif.insert(exif_byte, full_path)
            print(exif_dict)