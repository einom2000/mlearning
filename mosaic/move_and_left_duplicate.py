import os
import hashlib
import tkinter
from PIL import Image, ImageTk
from tkinter import ttk
from win32api import GetSystemMetrics
import math
import json
import shutil
import keyboard


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
    mpb["maximum"] = max_files_count
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


def build_zone_hash(size, hash=hashlib.sha1):
    hshs = {}
    if size in mother_folder_dictionary.keys():
        for file_path in mother_folder_dictionary[size]:
            hashobj = hash()
            for chunk in chunk_reader(open(file_path, 'rb')):
                hashobj.update(chunk)
            file_id = (hashobj.digest(), os.path.getsize(file_path))
            hshs[file_id] = file_path
    return hshs


def move_non_duplicated_file(cld_dir, mth_dir, hash=hashlib.sha1):
    global mother_folder_dictionary, count
    number = 1
    hashs = {}
    for dirpath, dirnames, filenames in os.walk(cld_dir):
        for filename in filenames:
            cld_path = os.path.join(child_dir, filename)
            st = os.stat(cld_path)
            size_zone = get_size_range(st.st_size)
            # build associated dictionary of hash
            hashs.clear()
            hashs = build_zone_hash(size_zone)
            # get current hash
            hashobj = hash()
            for chunk in chunk_reader(open(cld_path, 'rb')):
                hashobj.update(chunk)
            child_id = (hashobj.digest(), os.path.getsize(cld_path))
            duplicate_in_mother_dir = hashs.get(child_id, None)
            if duplicate_in_mother_dir:
                print(cld_path + ' has already in ' + mth_dir)
                print('identical file is ' + duplicate_in_mother_dir)
            else:
                tar_path = os.path.join(mth_dir, os.path.basename(cld_path))
                move_file(cld_path, tar_path)
                print('move ' + cld_path + ' to ' + tar_path)
                if size_zone in mother_folder_dictionary.keys():
                    mother_folder_dictionary[size_zone].append(tar_path)
                else:
                    mother_folder_dictionary[size_zone] = tar_path
                mother_folder_dictionary['files'] += 1
                count += 1

            number_text = str(number) + ' / ' + str(max_child_files)
            mpt = tkinter.Label(progress_gui, text=number_text)
            mpt2 = tkinter.Label(progress_gui, text=cld_path)
            mpt.place(x=300, y=40, anchor=tkinter.CENTER)
            mpt2.place(x=300, y=60, anchor=tkinter.CENTER)
            mpb["value"] += 1
            number += 1
            progress_gui.update()
# 2374

mother_dir = 'E:\\未整理，未与归档比较，有EXIF_1'  # F:\===================PIC TO CHECK\100NCD90
mother_folder_dictionary = {}
child_dir = 'E:\\未整理，未与归档比较，有EXIF__2'
count = 0

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
width_img = int(screen_width * 0.5)
height_img = int(screen_height * 0.5 -150)


progress_gui = tkinter.Tk()
progress_gui.geometry('%dx%d' % (600, 100))
bar_x = int((screen_width - 600 ) / 2)
progress_gui.geometry('+%d+%d' % (bar_x, 50))
progress_gui.title('checking images to move out the dulipcate ones')

max_files_count = count_files(mother_dir)
max_child_files = count_files(child_dir)
mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
mpb.pack()

dictionary_path = os.path.join(mother_dir, 'size_zone.json')

if os.path.isfile(dictionary_path):
#     with open(dictionary_path, 'r') as fp:
#         mother_folder_dictionary = json.load(fp)
#     if mother_folder_dictionary['files'] != max_files_count:
#         mother_folder_dictionary.clear()
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

