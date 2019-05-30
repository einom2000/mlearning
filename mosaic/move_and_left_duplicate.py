import os
import hashlib
import tkinter
from PIL import Image, ImageTk
from tkinter import ttk
from win32api import GetSystemMetrics
import math
import json
import shutil

def count_files(dir):
    cpt = sum([len(files) for r, d, files in os.walk(dir)])
    return cpt


def get_size_range(size_bytes):
    # [0, 100KB), [100KB, 200KB), [200KB, 300KB)....every 100KB
    k = math.ceil(size_bytes / (100 * 1000))
    return k


# make a dictionary by every 100KB,size
def build_dic(path):
    global mother_folder_dictionary
    count = 1
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
            pass
            count_text = str(count) + ' / ' + str(max_files_count)
            mpt = tkinter.Label(progress_gui, text=count_text)
            mpt2 = tkinter.Label(progress_gui, text=full_path)
            mpt.place(x=300, y=40, anchor=tkinter.CENTER)
            mpt2.place(x=300, y=60, anchor=tkinter.CENTER)
        mpb["value"] += 1
        count += 1
        progress_gui.update()



mother_dir = 'F:\\test'  # F:\===================PIC TO CHECK\100NCD90
mother_folder_dictionary = {}

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
mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
mpb.pack()

dictionary_path = os.path.join(mother_dir, 'size_zone.json')

if os.path.isfile(dictionary_path):
    with open(dictionary_path, 'r') as fp:
        mother_folder_dictionary = json.load(fp)
    if mother_folder_dictionary['files'] != max_files_count:
        mother_folder_dictionary.clear()
        shutil.



if not os.path.isfile(dictionary_path):
    build_dic(mother_dir)
    # add file number to dic
    mother_folder_dictionary['files'] = max_files_count + 1  # 'cause one json file
    with open(dictionary_path, 'w') as write_file:
        json.dump(mother_folder_dictionary, write_file, ensure_ascii=False)
    print(mother_folder_dictionary)
else:
    with open(dictionary_path, 'r') as fp:

        mother_folder_dictionary = json.load(fp)
        print(mother_folder_dictionary)
        print('-----------------------------')


