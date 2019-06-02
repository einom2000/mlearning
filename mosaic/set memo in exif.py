import piexif
import datetime
import os
import time
import tkinter
from win32api import GetSystemMetrics
from tkinter import ttk

dic = {
        'Title': b'Familey Memo',
        'Author': b'Exifed, dedupilcated, backuped',
        'CopyRight': 'singled and backuped on '
       }

tar_dir = 'F:\\已经备备_以后又增加_整理，更名，全EXIF相册，唯一'
# tar_dir = 'f:\\test'

count = 1
max_count = sum([len(files) for r, d, files in os.walk(tar_dir)])


screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

width_img = int(screen_width * 0.5)
height_img = int(screen_height * 0.5 -150)


progress_gui = tkinter.Tk()
progress_gui.geometry('%dx%d' % (600, 100))
bar_x = int((screen_width - 600 ) / 2)
progress_gui.geometry('+%d+%d' % (bar_x, 50))
progress_gui.title('adding today to exif and mark it as backed-up')

mpb = ttk.Progressbar(progress_gui, orient="horizontal", length=600, mode="determinate")
mpb.pack()
mpb["maximum"] = max_count
mpb["value"] = count


for dirpath, dirnames, filenames in os.walk(tar_dir):
    for filename in filenames:
        # print('Handling %d in total %d files.' % (count, max_count))
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
            # for ifd_name in exif_dict:
            #     # print('=======================================')
            #     # print("\n{0} IFD:".format(ifd_name))
            #     if exif_dict[ifd_name] is not None:
            #         for key in exif_dict[ifd_name]:
            #             # print(str(key) + ': ', end='')
            #             # print(exif_dict[ifd_name][key])
            #             pass
            #     else:
            #         print('None')

            if '0th' not in exif_dict.keys():
                exif_dict['0th'] = {}
            if 270 not in exif_dict['0th'].keys():
                exif_dict['0th'][270] = b''
            if 315 not in exif_dict['0th'].keys():
                exif_dict['0th'][315] = b''
            if 33432 not in exif_dict['0th'].keys():
                exif_dict['0th'][33432] = b''
            if 'thumbnail' in exif_dict.keys():
                _ = exif_dict.pop('thumbnail', None)


            if exif_dict['0th'][270] != dic['Title']:
                today = datetime.datetime.strftime(datetime.datetime.now(), "%Y:%m:%d %H:%M:%S")
                exif_dict['0th'][270] = dic['Title']
                exif_dict['0th'][315] = dic['Author']
                exif_dict['0th'][33432] = str.encode(dic['CopyRight'] + today)
                exif_byte = piexif.dump(exif_dict)
                piexif.insert(exif_byte, full_path)
                print(full_path)

            count_text = str(count) + ' / ' + str(max_count)
            mpt = tkinter.Label(progress_gui, text=count_text)
            mpt2 = tkinter.Label(progress_gui, text=full_path)
            mpt.place(x=300, y=40, anchor=tkinter.CENTER)
            mpt2.place(x=300, y=60, anchor=tkinter.CENTER)
        mpb["value"] += 1

        progress_gui.update()