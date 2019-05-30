import sys
import os
import hashlib
from PIL import Image, ImageTk
import numpy as np
import psutil
import keyboard
import os, sys
import tkinter
from win32api import GetSystemMetrics
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import math
import piexif
import shutil
import time
from tkinter import ttk
import cv2

# 检查重复需要吧原来的文件移动走进2个目录，需要考虑一下
#
# 需要进度条，计算总数和在进行数                                                               ----done

# 要做人脸识别，没有人脸和有人脸的 PHOTO / PIC
# 做时间检测，同一天的照片，提供筛选 PHOTO
# 没有人脸的照片。。。如何再区分
# 要把1970的日期清空
# 有EXIF的，有人脸的，按人物归类， 有些归类文档可以添加GPS。


def count_files(dir):
    cpt = sum([len(files) for r, d, files in os.walk(dir)])
    return cpt


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


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def string_2_ucs2(string):
    ucs2 = ()
    for b in bytearray(string):
        ucs2 += (b,0)
    return ucs2 + (0 ,0)


def insert_exif(fn, xpcomment):
    exif_dic = piexif.load(fn)
    # exif_dic['0th'][270] = 'this is a test'
    exif_dic['0th'][33432] = xpcomment   #string_2_ucs2(xpcomment.encode('utf-8'))
    try:
        new_exif_dic = piexif.dump(exif_dic)
    except ValueError:
        del exif_dic["thumbnail"]
        new_exif_dic = piexif.dump(exif_dic)
    piexif.insert(new_exif_dic, fn)


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    if info is not None:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    else:
        return None


def file_info(fn):
    st = os.stat(fn)
    size = convert_size(st.st_size)

    return datetime.strftime(datetime.fromtimestamp(st.st_ctime), "%Y-%m-%d %H:%M:%S"), \
           datetime.strftime(datetime.fromtimestamp(st.st_mtime), "%Y-%m-%d %H:%M:%S"), \
           size


def photo_info(fn):

    exif_datetime = 'Not Available'
    s = 'Not Available'
    gpsinfo = 'Not Available'

    data = get_exif(fn)

    if data is not None:
        # 3 time stamps
        time_keys = ['DateTimeOriginal',
                     'DateTimeDigitized',
                     'DateTime']

        for key in time_keys:
            if key in data.keys():
                d = datetime.strptime(data[key], "%Y:%m:%d %H:%M:%S")
                if exif_datetime == 'Not Available' or exif_datetime > d:
                    exif_datetime = d
        if exif_datetime != 'Not Available':
            exif_datetime = exif_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # original size
        exif_sizes = ['ExifImageWidth', 'ExifImageHeight']
        if exif_sizes[0] in data.keys() and exif_sizes[1] in data.keys():
            s = str(int(data[exif_sizes[0]])) + ' * ' + str(int(data[exif_sizes[1]]))

        # GPS info
        if 'GPSIno' in data.keys():
            for key in data['GPSInfo'].keys():
                decode = GPSTAGS.get(key, key)
                gpsinfo[decode] = data['GPSInfo'][key]

    ct, mt, sz = file_info(fn)
    return exif_datetime, s, str(gpsinfo), ct, mt, sz


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def check_for_duplicates(paths, hash=hashlib.sha1):
    hashes = {}

    for path in paths:
        count = 1
        max_files_count = count_files(path)
        mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
        mpb.pack()
        mpb["maximum"] = max_files_count
        mpb["value"] = count
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if True:  # int(filename[:5]) >= 14829:
                    extension = os.path.splitext(filename)[1][1:]
                    full_path = os.path.join(dirpath, filename)
                    if extension.lower() in file_type:
                        # try:
                            im = Image.open(full_path)
                            im.close()
                            hashobj = hash()
                            for chunk in chunk_reader(open(full_path, 'rb')):
                                hashobj.update(chunk)
                            file_id = (hashobj.digest(), os.path.getsize(full_path))
                            duplicate = hashes.get(file_id, None)
                            if duplicate:
                                # try:
                                    img1 = Image.open(duplicate)
                                    img2 = Image.open(full_path)

                                    img1_path = duplicate[len(path):]
                                    img2_path = full_path[len(path):]

                                    # create seperating zone
                                    img3 = Image.new('RGB', (30, img1.size[1]), color='gray')
                                    # merge imgs
                                    img = Image.new('RGB', (img1.size[0] + 30 + img2.size[0], img1.size[1]))
                                    img.paste(img1, (0, 0))
                                    img.paste(img3, (img1.size[0], 0))
                                    img.paste(img2, (img1.size[0] + 30, 0))
                                    # resize to fit screen
                                    ratio = img.size[0] / img.size[1]
                                    if ratio < 1 and img.size[1] >= height_img:
                                        img = img.resize((int(height_img * ratio), height_img), Image.ANTIALIAS)
                                    if ratio >= 1 and img.size[0] >= width_img:
                                        img = img.resize((width_img, int(width_img // ratio)), Image.ANTIALIAS)
                                    start_x = int((screen_width - img.size[0]) / 2)
                                    start_y = int((screen_height - img.size[1] - 150) / 2)

                                    root = tkinter.Toplevel()
                                    root.geometry('+%d+%d' % (start_x, start_y))
                                    root.geometry('%dx%d' % (img.size[0], img.size[1] + 150))
                                    tkpi = ImageTk.PhotoImage(img)
                                    label_image = tkinter.Label(root, image=tkpi)
                                    label_image.place(x=0, y=0, width=img.size[0], height=img.size[1])
                                    # show exif info
                                    img1_data = photo_info(duplicate)
                                    img2_data = photo_info(full_path)
                                    info_title = 'exif_datetime: ' + '\n' \
                                                + 'exif_size: ' + '\n' \
                                                + 'GPS info: ' + '\n' \
                                                + 'scan_dir: ' + '\n' \
                                                + 'sub_dir:' + '\n' \
                                                + 'create time: ' + '\n' \
                                                + 'last modify: ' + '\n' \
                                                + 'size:          '
                                    img1_info = img1_data[0] + '\n' \
                                                + img1_data[1] + '\n' \
                                                + img1_data[2] + '\n' \
                                                + path + '\n' \
                                                + img1_path + '\n' \
                                                + img1_data[3]+ '\n' \
                                                + img1_data[4]+ '\n' \
                                                + img1_data[5]
                                    img2_info = img2_data[0] + '\n' \
                                                + img2_data[1] + '\n' \
                                                + img2_data[2] + '\n' \
                                                + path + '\n' \
                                                + img2_path + '\n' \
                                                + img2_data[3]+ '\n' \
                                                + img2_data[4]+ '\n' \
                                                + img2_data[5]
                                    label_info_title = tkinter.Label(root, text=info_title, justify=tkinter.LEFT,
                                                                     compound=tkinter.LEFT)
                                    label_info_title.place(x=0, y=img.size[1])
                                    label_info_title2 = tkinter.Label(root, text=info_title, justify=tkinter.LEFT,
                                                                      compound=tkinter.LEFT)
                                    label_info_title2.place(x=int(img.size[0] / 2), y=img.size[1])
                                    lable_info_text = tkinter.Label(root, text=img1_info, justify=tkinter.LEFT,
                                                                    compound=tkinter.LEFT)
                                    lable_info_text.place(x=90, y=img.size[1])
                                    lable_info_text2 = tkinter.Label(root, text=img2_info, justify=tkinter.LEFT,
                                                                     compound=tkinter.LEFT)
                                    lable_info_text2.place(x=int(img.size[0] / 2) + 90, y=img.size[1])

                                    # show big red cross
                                    label_delete = tkinter.Label(root, text='XX', fg='red', font=('Times', 40),
                                                                 justify=tkinter.LEFT, compound=tkinter.LEFT)
                                    label_delete.place(x=int(img.size[0] - 90), y=int(img.size[1]))
                                    root.title('重复图片_按空格删除移动右侧图片到垃圾箱')
                                    root.update()
                                    target_file = os.path.join(duplicated_trash_dir, filename)
                                    move_file(full_path, target_file)
                                    time.sleep(.2)
                                    root.destroy()
                                    # move file
                                    print("Duplicate found: %s and %s" % (full_path, duplicate))
                                    print('Dulplicated file: % s moved to %s ' % (duplicate, duplicated_trash_dir))
                                # except OSError:
                                #    pass
                            else:
                                hashes[file_id] = full_path
                        #         exif = photo_info(full_path)
                        #         if exif[0] != 'Not Available' and int(exif[0][:4]) > 1972: #timestamp from 1970
                        #             arranged_file_name = str(int(datetime.timestamp(datetime.strptime(exif[0],
                        #                                                             "%Y-%m-%d %H:%M:%S"))))
                        #             target_file = os.path.join(photo_with_exif, arranged_file_name +'.' + extension)
                        #             move_file(full_path, target_file)
                        #
                        #             insert_exif(target_file, 'no duplicated copy before ' + today )
                        #         else:
                        #             target_file = os.path.join(pic_without_exif, filename)
                        #             move_file(full_path, target_file)
                        #     # keyboard.wait(' ')
                        # except OSError:
                        #     pass
                    count_text = str(count) + ' / ' + str(max_files_count)
                    mpt = tkinter.Label(progress_gui, text=count_text)
                    mpt2 = tkinter.Label(progress_gui, text=full_path)
                    mpt.place(x=300, y=40, anchor = tkinter.CENTER)
                    mpt2.place(x=300, y=60, anchor = tkinter.CENTER)
                mpb["value"] += 1
                count += 1
                progress_gui.update()


def face_recognition(pic_path):

    image = cv2.imread(pic_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 6)

        height, width, channels = image.shape
        images = cv2.resize(image, (800, int((800 / width) * height)))
        cv2.imshow('face found', images)
        cv2.waitKey(0)
        return True
    else:
        return False


def check_for_face(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            checking_file_path = os.path.join(path, filename)
            print(face_recognition(checking_file_path))





# cascPath = "C:\\Users\\einom\\PycharmProjects\\mlearning\\mosaic\\opencv_lib\\haarcascade_frontalface_default.xml"
cascPath = "C:\\Users\\einom\\PycharmProjects\\mlearning\\mosaic\\opencv_lib\\haarcascade_profileface.xml"
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

width_img = int(screen_width * 0.5)
height_img = int(screen_height * 0.5 -150)


progress_gui = tkinter.Tk()
progress_gui.geometry('%dx%d' % (600, 100))
bar_x = int((screen_width - 600 ) / 2)
progress_gui.geometry('+%d+%d' % (bar_x, 50))
progress_gui.title('checking images')


target_dir = 'F:\\________________pic_without_exif'  # F:\===================PIC TO CHECK\100NCD90

# create 3 sorts of folders  1, duplicated, 2, photo with exif, and 3 photo without exif
duplicated_trash_dir = target_dir[0:3] + 'DULIPCATED_PICS_TRASH_BIN_2'
photo_with_exif = target_dir[0:3] + 'WELL_ARRANGED_AND_TAGGED_PHOTOS'
pic_without_exif = target_dir[0:3] + 'pic_without_exif'
create_folder(duplicated_trash_dir)
create_folder(photo_with_exif)
create_folder(pic_without_exif)
today = str(datetime.today().date())

file_type = ['jpg', 'png', 'bmp', 'jpeg', 'tiff']

check_for_duplicates([target_dir, ])
# faced_file_dir = os.path.join(photo_with_exif, '\\photo_with_face')
# check_for_face(photo_with_exif)


