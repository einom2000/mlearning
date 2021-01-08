import os
import shutil

target_sh_dir = '\\\\WOW2070\\vipdoc\\sh\\lday'

target_sz_dir = '\\\\WOW2070\\vipdoc\\sz\\lday'

source_sh_dir = 'D:\\new_ajzq_v6\\vipdoc\\sh\\lday'

source_sz_dir = 'D:\\new_ajzq_v6\\vipdoc\\sz\\lday'


src_files = os.listdir(source_sh_dir)
files = len(src_files)
i = 0
for file_name in src_files:
    full_file_name = os.path.join(source_sh_dir, file_name)
    dest = os.path.join(target_sh_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, dest)
        i += 1
        files_left = files - i
        print(f'{files_left} files of {files} of sh remains to be copied.')


src_files = os.listdir(source_sz_dir)
files = len(src_files)
i = 0
for file_name in src_files:
    full_file_name = os.path.join(source_sz_dir, file_name)
    dest = os.path.join(target_sz_dir, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, dest)
        i += 1
        files_left = files - i
        print(f'{files_left} files of {files} of sz remains to be copied.')

