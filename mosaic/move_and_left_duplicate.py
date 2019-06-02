import os
import hashlib
import tkinter
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS, GPSTAGS
from tkinter import ttk
from win32api import GetSystemMetrics
import math
import json
import shutil
import keyboard
from PIL import Image, ImageTk
from datetime import datetime
import time


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


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


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
                d = datetime.strptime(data[key][:19], "%Y:%m:%d %H:%M:%S")
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
    return tar1

def count_files(dir):
    cpt = sum([len(files) for r, d, files in os.walk(dir)])
    return cpt


def get_size_range(size_bytes):
    # [0, 100KB), [100KB, 200KB), [200KB, 300KB)....every 100KB
    k = math.ceil(size_bytes / (100 * 1000))
    return str(k)


# make a dictionary by every 100KB,size
def build_dic(path):
    global mother_folder_dictionary
    mpb["maximum"] = max_child_files
    mpb["value"] = count
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(path, filename)
            st = os.stat(full_path)
            size_range = get_size_range(st.st_size)
            if size_range not in mother_folder_dictionary.keys():
                mother_folder_dictionary[size_range] = []
            mother_folder_dictionary[size_range].append(full_path)


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def build_zone_hash(size, hash=hashlib.sha1, add_full_path=None):
    global mother_folder_dictionary, hashes
    if size not in hashes.keys():
        hashes[size] = {}
        if size in mother_folder_dictionary.keys():
            for file_path in mother_folder_dictionary[size]:
                hashobj = hash()
                for chunk in chunk_reader(open(file_path, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(file_path))
                if file_id not in hashes[size].keys():
                    hashes[size][file_id] = file_path
    if add_full_path is not None:
            hashobj = hash()
            for chunk in chunk_reader(open(add_full_path, 'rb')):
                hashobj.update(chunk)
            file_id = (hashobj.digest(), os.path.getsize(add_full_path))
            if file_id not in hashes[size].keys():
                hashes[size][file_id] = add_full_path

def move_non_duplicated_file(cld_dir, mth_dir, hash=hashlib.sha1):
    global mother_folder_dictionary, count, hashes
    number = 1
    for dirpath, dirnames, filenames in os.walk(cld_dir):
        for filename in filenames:
            cld_path = os.path.join(child_dir, filename)
            st = os.stat(cld_path)
            size_zone = get_size_range(st.st_size)
            # build associated dictionary of hash
            build_zone_hash(size_zone)
            # get current hash
            hashobj = hash()
            for chunk in chunk_reader(open(cld_path, 'rb')):
                hashobj.update(chunk)
            child_id = (hashobj.digest(), os.path.getsize(cld_path))
            duplicate_in_mother_dir = hashes[size_zone].get(child_id, None)
            if duplicate_in_mother_dir:
                if show_identical:
                    img1 = Image.open(duplicate_in_mother_dir)
                    img2 = Image.open(cld_path)
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
                    img1_data = photo_info(duplicate_in_mother_dir)
                    img2_data = photo_info(cld_path)
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
                                + mother_dir + '\n' \
                                + duplicate_in_mother_dir + '\n' \
                                + img1_data[3] + '\n' \
                                + img1_data[4] + '\n' \
                                + img1_data[5]
                    img2_info = img2_data[0] + '\n' \
                                + img2_data[1] + '\n' \
                                + img2_data[2] + '\n' \
                                + cld_dir + '\n' \
                                + cld_path + '\n' \
                                + img2_data[3] + '\n' \
                                + img2_data[4] + '\n' \
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
                    root.title('重复图片_')
                    root.update()
                    keyboard.wait(0)
                    root.destroy()
                print(cld_path + ' has already in ' + mth_dir)
                print('identical file is ' + duplicate_in_mother_dir)
            else:
                tar_path = os.path.join(mth_dir, os.path.basename(cld_path))
                moved_tar = move_file(cld_path, tar_path)
                print('move ' + cld_path + ' to ' + tar_path)
                if size_zone in mother_folder_dictionary.keys():
                    mother_folder_dictionary[size_zone].append(moved_tar)
                else:
                    mother_folder_dictionary[size_zone] = [moved_tar,]
                build_zone_hash(size_zone, add_full_path=moved_tar)
                mother_folder_dictionary['files'] += 1

            number_text = str(number) + ' / ' + str(max_child_files)
            mpt = tkinter.Label(progress_gui, text=number_text)
            mpt2 = tkinter.Label(progress_gui, text=' '* 30 + cld_path + ' ' * 30)
            mpt.place(x=300, y=40, anchor=tkinter.CENTER)
            mpt2.place(x=300, y=60, anchor=tkinter.CENTER)
            number += 1
            mpb["value"] = number
            progress_gui.update()
# 2374


mother_dir = 'E:\\未备备_有添加合并_整理，更名，全EXIF相册，唯一'  # F:\===================PIC TO CHECK\100NCD90
mother_folder_dictionary = {}
child_dir = 'E:\\PHOTO_WITH_EXIF_网盘全部下载部分'
count = 0
hashes = {}
show_identical = True

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
width_img = int(screen_width * 0.5)
height_img = int(screen_height * 0.5 - 150)

progress_gui = tkinter.Tk()
progress_gui.geometry('%dx%d' % (600, 100))
bar_x = int((screen_width - 600) / 2)
progress_gui.geometry('+%d+%d' % (bar_x, 50))
progress_gui.title('checking images to move out the dulipcate ones')

max_files_count = count_files(mother_dir)
max_child_files = count_files(child_dir)
mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
mpb.pack()

dictionary_path = os.path.join(mother_dir, 'size_zone.json')

if os.path.isfile(dictionary_path):
    os.remove(dictionary_path)

if mother_folder_dictionary == {}:
    build_dic(mother_dir)
    # add file number to dic
    mother_folder_dictionary['files'] = max_files_count + 1  # 'cause one json file
    with open(dictionary_path, 'w') as write_file:
        json.dump(mother_folder_dictionary, write_file, ensure_ascii=False)

move_non_duplicated_file(child_dir, mother_dir)

last_mother_files = count_files(mother_dir)
last_child_files = count_files(child_dir)

print(str(count) + ' files has been moved')
print(mother_dir + ' from ' + str(max_files_count) + ' up to ' + str(last_mother_files) + ' files')
print(child_dir + ' from ' + str(max_child_files) + ' down to ' + str(last_child_files) + ' files')
print(str(max_child_files - last_child_files) + ' are unique ')

