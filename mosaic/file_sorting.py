import sys
import os
import hashlib
from PIL import Image, ImageTk
import numpy as np
import psutil
import keyboard
import os, sys
import tkinter



def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.


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
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                extension = os.path.splitext(filename)[1][1:]
                if extension.lower() in file_type:
                    full_path = os.path.join(dirpath, filename)
                    hashobj = hash()
                    for chunk in chunk_reader(open(full_path, 'rb')):
                        hashobj.update(chunk)
                    file_id = (hashobj.digest(), os.path.getsize(full_path))
                    duplicate = hashes.get(file_id, None)
                    if duplicate:
                        img1 = Image.open(full_path)
                        img2 = Image.open(duplicate)
                        img = Image.fromarray(np.hstack((np.array(img1), np.array(img2))))
                        root.geometry('%dx%d' % (img.size[0], img.size[1]))
                        tkpi = ImageTk.PhotoImage(img)
                        label_image = tkinter.Label(root, image=tkpi)
                        label_image.place(x=0, y=0, width=img.size[0], height=img.size[1])
                        root.title(duplicate)
                        root.update()
                        keyboard.wait(' ')
                        label_image.destroy()
                        for proc in psutil.process_iter():
                            if proc.name() == "Photos":
                                proc.kill()
                        print("Duplicate found: %s and %s" % (full_path, duplicate))
                    else:
                        hashes[file_id] = full_path







root = tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
root.geometry('+%d+%d' % (100,100))

file_type = ['jpg', 'png', 'gif', 'bmp', 'jpeg', 'tiff']
check_for_duplicates(['e:\\einom\\Pictures', ])



