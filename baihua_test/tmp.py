# import re
#
# a = 'a+b+c+d=100[10, 99]'
# x = re.sub('[a-zA-Z]', '', a)
#
# print(x)

import getpass, os
USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
        print(file_path)
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)

add_to_startup('python c:\\myip.py')