import datetime
import os
import piexif
import shutil
import time
import sys

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


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def return_FileModifyDate(file_path):
    cmd = 'c:\\windows\\exiftool_win.exe -s -G -FileModifyDate ' + file_path + '>' + target_dir + '\\temp\\111.txt'
    os.popen(cmd).read()

    with open(target_dir + '\\temp\\111.txt') as f:
        first_line = f.readline().replace(' ', '')
        print(first_line)
    if len(first_line) >= 40:
        createtime = first_line[-25:-7]
        return createtime
    else:
        return None

def return_media_created_time(file_path, cmd, utc=True):
    os.popen(cmd).read()
    with open(target_dir + '\\temp\\111.txt') as f:
        first_line = f.readline().replace(' ', '')
        print(first_line)
        print(first_line[-7])
    if len(first_line) >= 40:
        if first_line[-7] == '+':
            createtime = first_line[-25: -7]
            print(first_line[-25: -7])
        else:
            createtime = first_line[-19:-1]
            print(first_line[-19:-1])
        if createtime == '0000:00:0000:00:00':
            return 'zero'
        # try:
        if utc is True:
            createtime = datetime.datetime.strptime(createtime, "%Y:%m:%d%H:%M:%S")
            local_createtime = datetime_from_utc_to_local(createtime)
            return local_createtime
        else:
            local_createtime = datetime.datetime.strptime(createtime, "%Y:%m:%d%H:%M:%S")
            return local_createtime
        # except ValueError:
            # return None
    else:
        return None


target_dir = 'F:\\test'
tmp_dir = 'f:\\test2'

pre_fix = ''
create_folder(tmp_dir)
temp_dir = target_dir + '\\temp'
create_folder(temp_dir)

for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        if filename[:len(pre_fix)] == pre_fix and (os.path.splitext(filename)[1][1:].lower() == 'mp4' or
                                                   os.path.splitext(filename)[1][1:].lower() == 'avi') :
            # try:
                original_path = os.path.join(target_dir, filename)
                ext = os.path.splitext(filename)[1]
                # following is name with datetime
                # print(filename[len(pre_fix): 14 + len(pre_fix) - 0])
                # t = datetime.datetime.strptime(filename[len(pre_fix): 14 + len(pre_fix) - 0], "%Y%m%d%H%M%S")


                # fllowing is name start with datetime without any prefix
                # print(filename[: 16])
                # t = datetime.datetime.strptime(filename[:16], "%Y_%m%d_%H%M%S")


                # following is name with timestamp
                # ts = float(filename[len(pre_fix): len(pre_fix) + 13]) / 1000
                # t = datetime.datetime.fromtimestamp(ts)


                # following is name with timestamp without any prefix
                # ts = float(filename[: 10])
                # # t = datetime.datetime.fromtimestamp(ts)

                # following is to get the CreateDate from the media file and turn it to local timestamp
                if os.path.splitext(filename)[1][1:].lower() == 'mp4':
                    cd1 = 'c:\\windows\\exiftool_win.exe -s -G -CreateDate ' + original_path\
                         + '>' + target_dir + '\\temp\\111.txt'
                if os.path.splitext(filename)[1][1:].lower() == 'avi':
                    cd1 = 'c:\\windows\\exiftool_win.exe -s -G -DateTimeOriginal ' + original_path\
                         + '>' + target_dir + '\\temp\\111.txt'
                tempdate = return_media_created_time(original_path, cd1)
                if tempdate == 'zero':
                    cd2 = 'c:\\windows\\exiftool_win.exe \"-FileModifyDate>CreateDate\" ' + original_path
                    os.popen(cd2).read()
                    tempdate = return_media_created_time(original_path, cd1, utc=False)
                if tempdate is not None:
                    print(tempdate)
                    new_filename = str(int(datetime.datetime.timestamp(tempdate))) + ext
                    print(new_filename)

                    # new_filename = str(int(datetime.datetime.timestamp(t))) + ext
                    new_path = os.path.join(tmp_dir, new_filename)
                    # print(t)
                    print(original_path)
                    print(new_path)
                    move_file(original_path, new_path)
                    # set_datetime_exif(new_path, t)
            #
            # except TypeError:
            #     pass
