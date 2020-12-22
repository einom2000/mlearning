# import tensorflow as tf
import os
from struct import *


def day2csv_data(dirname, fname, targetDir, starttime=20100101, market='sh'):
    ofile = open(os.path.join(dirname.replace('mkt', market), fname), 'rb')
    buf = ofile.read()
    ofile.close()

    ifile = open(os.path.join(targetDir.replace('mkt', market), fname[:-4]) + '.csv', 'w')
    num = len(buf)
    no = num / 32
    b = 0
    e = 32
    line = ''
    linename = str('') + ',' + str('open') + ',' + str('high') + ',' + str('low') + ',' + str(
        'adjclose') + ',' + str('amount') + ',' + str('volume') + ',' + str('str07') + '' + '\n'
    # print line
    ifile.write(linename)
    # for i in xrange(no):
    for i in range(int(no)):
        a = unpack('IIIIIfII', buf[b:e])
        if a[0] >= starttime:
            date = str(a[0])
            date = date[:4] + '-' + date[4:6] + '-' + date[-2:]
            line = date + ',' + str(a[1] / 100.0) + ',' + str(a[2] / 100.0) + ',' + str(a[3] / 100.0) + ',' + str(
                a[4] / 100.0) + ',' + str(a[5]) + ',' + str(a[6]) + ',' + str(a[7]) + '' + '\n'
            # print line
            ifile.write(line)
        b = b + 32
        e = e + 32
    ifile.close()

pathdir = "d:\\vipdoc\\mkt\\lday"
targetDir = "d:\\vipdoc\\mkt\\lday_csv"

# listfile = os.listdir(pathdir)
#
# for f in listfile:
#     day2csv_data(pathdir, f, targetDir)
#     print(f, end='Done! ')
# else:
#     print('The for ' + pathdir + ' to ' + targetDir + '  loop is over')
# print()

day2csv_data("d:\\vipdoc\\mkt\\lday", 'sh600600.day', "", starttime=20000101, market='sh')




