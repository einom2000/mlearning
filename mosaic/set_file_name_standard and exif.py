import datetime
import os
import piexif
import shutil
import keyboard


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


target_dir = 'F:\\整理，无EXIF相册，唯一， 未更名 2019_05_30'
tmp_dir = 'F:\\tmp'

pre_fix = 'DSC_0024_mh'
create_folder(tmp_dir)

for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        if filename[:len(pre_fix)] == pre_fix:
            try:
                # following is name with datetime
                # print(filename[len(pre_fix): 19 + len(pre_fix) - 0])
                # t = datetime.datetime.strptime(filename[len(pre_fix): 19 + len(pre_fix) - 0], "%Y_%m_%d_%H_%M_%S")


                # fllowing is name start with datetime without any prefix
                # print(filename[: 17])
                # t = datetime.datetime.strptime(filename[:17], "%Y-%m-%d-%H%M%S")


                # following is name with timestamp
                # ts = float(filename[len(pre_fix): len(pre_fix) + 13]) / 1000
                # t = datetime.datetime.fromtimestamp(ts)


                # following is name with timestamp without any prefix
                # ts = float(filename[: 10])
                # t = datetime.datetime.fromtimestamp(ts)

                original_path = os.path.join(target_dir, filename)
                new_path = os.path.join(tmp_dir, filename)
                print(t)
                print(original_path)

                # move_file(original_path, new_path)
                # set_datetime_exif(new_path, t)

            except TypeError:
                pass
