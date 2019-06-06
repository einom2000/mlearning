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
import imageio
# 发现同一个目录里的相同文件，扫描数量不可太大


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


def save_frame_1(video_path, frame_image_name):
    video = imageio.get_reader(video_path)
    frame = 0
    for image in video.iter_data():
        frame += 1                                       #counter to save new frame number
        image_frame = Image.fromarray(image)
        print(frame_image_name)
        image_frame.save(frame_image_name)               #if you need the frame you can save each frame to hd
        frame_image = ImageTk.PhotoImage(image_frame)
        if frame == 1: break                             #after 40 frames stop, or remove this line for the entire video


#
# def insert_exif(fn, xpcomment):
#     exif_dic = piexif.load(fn)
#     # exif_dic['0th'][270] = 'this is a test'
#     exif_dic['0th'][33432] = xpcomment   #string_2_ucs2(xpcomment.encode('utf-8'))
#     try:
#         new_exif_dic = piexif.dump(exif_dic)
#     except ValueError:
#         del exif_dic["thumbnail"]
#         new_exif_dic = piexif.dump(exif_dic)
#     piexif.insert(new_exif_dic, fn)
#
#
# def get_exif(fn):
#     ret = {}
#     i = Image.open(fn)
#     info = i._getexif()
#     if info is not None:
#         for tag, value in info.items():
#             decoded = TAGS.get(tag, tag)
#             ret[decoded] = value
#         return ret
#     else:
#         return None


def file_info(fn):
    st = os.stat(fn)
    size = convert_size(st.st_size)

    return datetime.strftime(datetime.fromtimestamp(st.st_ctime), "%Y-%m-%d %H:%M:%S"), \
           datetime.strftime(datetime.fromtimestamp(st.st_mtime), "%Y-%m-%d %H:%M:%S"), \
           size


# def photo_info(fn):
#
#     exif_datetime = 'Not Available'
#     s = 'Not Available'
#     gpsinfo = 'Not Available'
#
#     data = get_exif(fn)
#
#     if data is not None:
#         # 3 time stamps
#         time_keys = ['DateTimeOriginal',
#                      'DateTimeDigitized',
#                      'DateTime']
#
#         for key in time_keys:
#             if key in data.keys():
#                 d = datetime.strptime(data[key][:19], "%Y:%m:%d %H:%M:%S")
#                 if exif_datetime == 'Not Available' or exif_datetime > d:
#                     exif_datetime = d
#         if exif_datetime != 'Not Available':
#             exif_datetime = exif_datetime.strftime("%Y-%m-%d %H:%M:%S")
#
#         # original size
#         exif_sizes = ['ExifImageWidth', 'ExifImageHeight']
#         if exif_sizes[0] in data.keys() and exif_sizes[1] in data.keys():
#             s = str(int(data[exif_sizes[0]])) + ' * ' + str(int(data[exif_sizes[1]]))
#
#         # GPS info
#         if 'GPSIno' in data.keys():
#             for key in data['GPSInfo'].keys():
#                 decode = GPSTAGS.get(key, key)
#                 gpsinfo[decode] = data['GPSInfo'][key]
#
#     ct, mt, sz = file_info(fn)
#     return exif_datetime, s, str(gpsinfo), ct, mt, sz


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def make_file_sizes_dictionary(tar_dir):
    dic = {}
    for dirpath, dirnames, filenames in os.walk(tar_dir):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            size = os.path.getsize(fullpath)
            if size not in dic.keys():
                dic[size] = [fullpath, ]
            else:
                dic[size].append(fullpath)

    return dic


def check_for_duplicates(paths, hash=hashlib.sha1):
    existing_file_path = None
    dic = {}
    for path in paths:
        count = 1
        max_files_count = count_files(path)
        mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
        mpb.pack()
        mpb["maximum"] = max_files_count
        mpb["value"] = count
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if 0 <= count :
                    extension = os.path.splitext(filename)[1][1:]
                    full_path = os.path.join(dirpath, filename)
                    if extension.lower() in file_type:
                        # try:
                            size = os.path.getsize(full_path)
                            if size not in dic.keys():
                                dic[size] = [full_path, ]
                            else:
                                duplicate = False
                                hashobj = hash()
                                for chunk in chunk_reader(open(full_path, 'rb')):
                                    hashobj.update(chunk)
                                file_id = hashobj.digest()

                                for existing_file in dic[size]:
                                    hashobj = hash()
                                    for chunk in chunk_reader(open(existing_file, 'rb')):
                                        hashobj.update(chunk)
                                    existing_file_id = hashobj.digest()
                                    if existing_file_id == file_id:
                                        duplicate = True
                                        existing_file_path = existing_file

                                if duplicate:
                                    # try:
                                        if show_identical:
                                            print(os.getcwd())
                                            existing_file_path_frame = os.getcwd() + '\\temp\\existing_frame.png'
                                            full_path_frame = os.getcwd() + '\\temp\\full_frame.png'
                                            print(existing_file_path_frame)
                                            print(full_path_frame)
                                            save_frame_1(existing_file_path, existing_file_path_frame)
                                            save_frame_1(full_path, full_path_frame)
                                            len1 = len(os.path.basename(existing_file_path))
                                            len2 = len(os.path.basename(full_path))
                                            if len1 > len2:
                                                existing_file_path_frame, full_path_frame \
                                                                = full_path_frame, existing_file_path_frame
                                                existing_file_path, full_path = full_path, existing_file_path

                                            img1 = Image.open(existing_file_path_frame)
                                            img2 = Image.open(full_path_frame)

                                            img1_path = existing_file_path[len(path):]
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
                                            # img1_data = photo_info(existing_file_path)
                                            # img2_data = photo_info(full_path)
                                            # info_title = 'exif_datetime: ' + '\n' \
                                            #             + 'exif_size: ' + '\n' \
                                            #             + 'GPS info: ' + '\n' \
                                            #             + 'scan_dir: ' + '\n' \
                                            #             + 'sub_dir:' + '\n' \
                                            #             + 'create time: ' + '\n' \
                                            #             + 'last modify: ' + '\n' \
                                            #             + 'size:          '
                                            # img1_info = img1_data[0] + '\n' \
                                            #             + img1_data[1] + '\n' \
                                            #             + img1_data[2] + '\n' \
                                            #             + path + '\n' \
                                            #             + img1_path + '\n' \
                                            #             + img1_data[3]+ '\n' \
                                            #             + img1_data[4]+ '\n' \
                                            #             + img1_data[5]
                                            # img2_info = img2_data[0] + '\n' \
                                            #             + img2_data[1] + '\n' \
                                            #             + img2_data[2] + '\n' \
                                            #             + path + '\n' \
                                            #             + img2_path + '\n' \
                                            #             + img2_data[3]+ '\n' \
                                            #             + img2_data[4]+ '\n' \
                                            #             + img2_data[5]
                                            # label_info_title = tkinter.Label(root, text=info_title, justify=tkinter.LEFT,
                                            #                                  compound=tkinter.LEFT)
                                            # label_info_title.place(x=0, y=img.size[1])
                                            # label_info_title2 = tkinter.Label(root, text=info_title, justify=tkinter.LEFT,
                                            #                                   compound=tkinter.LEFT)
                                            # label_info_title2.place(x=int(img.size[0] / 2), y=img.size[1])
                                            # lable_info_text = tkinter.Label(root, text=img1_info, justify=tkinter.LEFT,
                                            #                                 compound=tkinter.LEFT)
                                            # lable_info_text.place(x=90, y=img.size[1])
                                            # lable_info_text2 = tkinter.Label(root, text=img2_info, justify=tkinter.LEFT,
                                            #                                  compound=tkinter.LEFT)
                                            # lable_info_text2.place(x=int(img.size[0] / 2) + 90, y=img.size[1])

                                            # show big red cross
                                            label_delete = tkinter.Label(root, text='XX', fg='red', font=('Times', 40),
                                                                         justify=tkinter.LEFT, compound=tkinter.LEFT)
                                            label_delete.place(x=int(img.size[0] - 90), y=int(img.size[1]))
                                            root.title('重复图片_按空格删除移动右侧图片到垃圾箱')
                                            root.update()
                                            time.sleep(1)
                                            root.destroy()
                                        target_file = os.path.join(duplicated_trash_dir, os.path.basename(full_path))
                                        print(target_file)
                                        move_file(full_path, target_file)

                                        # move file
                                        print("Duplicate found: %s and %s" % (full_path, existing_file_path))
                                        print('Dulplicated file: % s moved to %s ' % (full_path, duplicated_trash_dir))
                                    # except OSError:
                                    #    pass
                                else:
                                    dic[size].append(full_path)
                                #     hashes[file_id] = full_path
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
                    mpt2 = tkinter.Label(progress_gui, text=' ' * 20 + full_path + ' ' * 20)
                    mpt.place(x=300, y=40, anchor = tkinter.CENTER)
                    mpt2.place(x=300, y=60, anchor = tkinter.CENTER)
                mpb["value"] += 1
                count += 1
                progress_gui.update()


show_identical = True

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

width_img = int(screen_width * 0.5)
height_img = int(screen_height * 0.5 -150)


progress_gui = tkinter.Tk()
progress_gui.geometry('%dx%d' % (600, 100))
bar_x = int((screen_width - 600 ) / 2)
progress_gui.geometry('+%d+%d' % (bar_x, 50))
progress_gui.title('checking images to move out the dulipcate ones')


target_dir = 'F:\\未备备，未整理未更名，未备注，唯一 MP4_1538files'  # F:\===================PIC TO CHECK\100NCD90

# create 3 sorts of folders  1, duplicated, 2, photo with exif, and 3 photo without exif
duplicated_trash_dir = os.path.join(target_dir[:3], 'DULIPCATED_PICS_TRASH_BIN_2')
create_folder(duplicated_trash_dir)
today = str(datetime.today().date())

file_type = ['mp4', ]

# file_sizes_dic = make_file_sizes_dictionary(target_dir)
# print(file_sizes_dic)
check_for_duplicates([target_dir, ])





