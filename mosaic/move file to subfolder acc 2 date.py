import datetime
import os
import piexif
import shutil
import keyboard


# 根据文件名归入时间文件夹

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


target_dir = 'G:\\___DOWNLOAD FROM BAIDU_CLEAN_BAIDU_2019_12_14\\tmp_mp4_sorted_routine_out\\tmp2'


pre_fix = 'OtherType'
files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

for filename in files:
    if filename[:9] != pre_fix:
        try:
            timestamp = int(filename[:10])
            full_path = os.path.join(target_dir, filename)
            time = datetime.datetime.fromtimestamp(timestamp)
            year_dir = os.path.join(target_dir, str(time.year) + '年')
            create_folder(year_dir)
            month_dir = os.path.join(year_dir,str(time.month) + '月')
            create_folder(month_dir)
            target_path = os.path.join(month_dir, filename)
            print(full_path, target_path)
            move_file(full_path, target_path)
        except:
            print(filename)




