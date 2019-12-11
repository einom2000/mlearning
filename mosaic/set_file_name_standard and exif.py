import datetime
import os
import shutil

import piexif


# 根据文件名人肉判断并修复exif

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def file_surffix(t, tar):
    t += 1
    if t < 1000:
        tx = '0' * (3 - len(str(t))) + str(t)
    else:
        tx = str(t)
    return os.path.splitext(tar)[0] + '_' + tx + os.path.splitext(tar)[1]


def move_file(src, tar):
    tar1 = tar
    if os.path.isfile(tar):
        t = 0
        tar1 = file_surffix(t, tar)
        while os.path.isfile(tar1):
            t += 1
            tar1 = file_surffix(t, tar)
    shutil.move(src, tar1)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! for safty reason, use copy while testing


def set_datetime_exif(fn, t):
    exif_dict = piexif.load(fn)
    str_t = datetime.datetime.strftime(t, "%Y:%m:%d %H:%M:%S")
    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: str_t,
                piexif.ExifIFD.LensMake: u"ManualSet",
                piexif.ExifIFD.Sharpness: 65535,
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                }
    exif_dict["Exif"] = exif_ifd
    exif_byte = piexif.dump(exif_dict)
    piexif.insert(exif_byte, fn)


target_dir = 'e:\\einom\Documents\\vedio rename temp'
tmp_dir = 'e:\\einom\\Documents\\vedio rename temp'

create_folder(tmp_dir)

for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        new_file_name = ''
        digits = '0123456789'
        for i in range(len(filename)):
            if len(filename) > 18 and filename.isdigit():
                new_file_name = filename[:12]
                new_file_name = '20' + new_file_name[-2:] + \
                                       new_file_name[-4:-2] + \
                                       new_file_name[-6:-4] + \
                                       new_file_name[:2] + \
                                       new_file_name[-8:-6] + \
                                       new_file_name[-10:-8]

                break
            if filename[i] == '.' and i >= len(filename) - 4:
                break
            if digits.find(filename[i]) != -1:
                new_file_name += filename[i]

        last_name = filename[filename.find('.', -5, -1):]
        print(new_file_name)

        t = 0
        # following is name with timestamp
        if len(new_file_name) == 13 and new_file_name[0] == '1':
            ts = float(new_file_name) / 1000
            t = datetime.datetime.fromtimestamp(ts)

        # following is name with datetime
        if new_file_name[:3] == '201' and len(new_file_name) >= 14:
            t = datetime.datetime.strptime(new_file_name[:14], "%Y%m%d%H%M%S")

        print(new_file_name)
        print(filename)

        if t != 0:
            original_path = os.path.join(target_dir, filename)
            ext = os.path.splitext(filename)[1]
            if ext == '.jpeg':
                ext = '.jpg'
            if ext: # == '.jpg':
                new_filename = str(int(datetime.datetime.timestamp(t))) + ext
                new_path = os.path.join(tmp_dir, new_filename)
                print(original_path)
                print(new_path)

                move_file(original_path, new_path)
                # set_datetime_exif(new_path, t)

        #
        #
        #
        # # if filename[:len(pre_fix)] == pre_fix:
        # #     try:
        # #         # following is name with datetime
        # #         # print(filename[len(pre_fix): 19 + len(pre_fix) - 0])
        # #         # t = datetime.datetime.strptime(filename[len(pre_fix): 19 + len(pre_fix) - 0], "%Y_%m_%d_%H_%M_%S")
        # #
        # #
        # #         # fllowing is name start with datetime without any prefix
        # #         # print(filename[: 17])
        # #         # t = datetime.datetime.strptime(filename[:17], "%Y-%m-%d-%H%M%S")
        # #
        # #
        # #         # following is name with timestamp
        # #         # ts = float(filename[len(pre_fix): len(pre_fix) + 13]) / 1000
        # #         # t = datetime.datetime.fromtimestamp(ts)
        # #
        # #
        # #         # following is name with timestamp without any prefix
        # #         ts = float(filename[: 10])
        # #         t = datetime.datetime.fromtimestamp(ts)
        # #
        # #         original_path = os.path.join(target_dir, filename)
        # #         ext = os.path.splitext(filename)[1]
        # #         if ext == '.jpeg':
        # #             ext = '.jpg'
        # #         new_filename = str(int(datetime.datetime.timestamp(t))) + ext
        # #         new_path = os.path.join(tmp_dir, new_filename)
        # #         print(t)
        # #         print(original_path)
        # #         print(new_path)
        # #
        # #         move_file(original_path, new_path)
        # #         set_datetime_exif(new_path, t)
        #
        #     # except TypeError:
        #     #     pass
    break
