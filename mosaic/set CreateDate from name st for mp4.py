import piexif
import datetime
import os
import time
import tkinter
from win32api import GetSystemMetrics
from tkinter import ttk
import sys
import keyboard

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


tar_dir = 'F:\\from_here'
temp_dir = tar_dir + '\\temp'
create_folder(temp_dir)

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
        if os.path.splitext(filename)[1][1:].lower() == 'mp4':
                full_path = os.path.join(dirpath, filename)
            # print(full_path)
            # try:
            #     exif_dict = piexif.load(full_path)
            #
            #     # print(exif_dict)
                if os.stat(full_path).st_mode == 33060:
                    os.chmod(full_path, 33206)
                cd1 = 'c:\\windows\\exiftool_win.exe -s -G -CreateDate ' + full_path \
                      + '>' + tar_dir + '\\temp\\111.txt'
                os.popen(cd1).read()
                with open(tar_dir + '\\temp\\111.txt') as f:
                    first_line = f.readline().replace(' ', '')
                createtime = 1970
                if len(first_line) >= 20:
                    try:
                        le = first_line.index('Date')
                        createtime = int(first_line[le + 5: le + 9])
                    except ValueError:
                        print(first_line)
                        print(first_line[le + 5: le + 9])
                        print(full_path)
                        keyboard.wait(0)
                if createtime <= 2010:
                    print(first_line)
                    print(full_path)
                    create_date = datetime.datetime.fromtimestamp(int(os.path.splitext(filename)[0]))
                    create_date -= datetime.timedelta(hours=8)
                    create_date = str(create_date).replace(' ', '')
                    cmd = 'c:\\windows\\exiftool_win.exe -CreateDate=' + create_date + ' ' + full_path
                    os.popen(cmd).read()
                    print(full_path + ' CreateDate = ' + create_date + ' is Done!')

                count_text = str(count) + ' / ' + str(max_count)
                mpt = tkinter.Label(progress_gui, text=count_text)
                mpt2 = tkinter.Label(progress_gui, text=' ' * 20 +full_path + ' ' * 20)
                mpt.place(x=300, y=40, anchor=tkinter.CENTER)
                mpt2.place(x=300, y=60, anchor=tkinter.CENTER)
                mpb["value"] += 1

                progress_gui.update()
            # except:
            #     print(full_path)
            #     print('press any key to delete')
            #     # keyboard.wait(0)
            #     continue