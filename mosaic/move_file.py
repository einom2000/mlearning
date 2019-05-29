import os
import shutil


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


src_path = 'F:\\pic_without_exif'
tar_path = 'F:\\________________pic_without_exif'


for dirpath, dirnames, filenames in os.walk(src_path):
    for filename in filenames:
        scr_file = os.path.join(src_path, filename)
        tar_file = os.path.join(tar_path, filename)
        move_file(scr_file, tar_file)
