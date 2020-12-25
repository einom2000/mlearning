import os
import time
from struct import *


def day2csv_data(dirname, fname, targetDir, starttime=20050104, market='sh'):
    try:
        ofile = open(os.path.join(dirname.replace('mkt', market), fname), 'rb')
        buf = ofile.read()
        ofile.close()

        ifile = open(os.path.join(targetDir.replace('mkt', market), fname[:-4]) + '_' +
                     time.strftime("%Y-%m-%d") + '.csv', 'w')
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
        return os.path.join(targetDir.replace('mkt', market), fname[:-4]) + '.csv'
    except FileNotFoundError:
        print(os.path.join(dirname.replace('mkt', market)))
        return False


def day_to_csv(single_code=None, single_target_dir="csv-original\\", market='sh', starttime=20050104,
               pathdir="d:\\new_ajzq_v6\\vipdoc\\mkt\\lday"):

    if single_code is None:

        targetDir = "d:\\vipdoc\\mkt\\lday_csv"

        listfile = os.listdir(pathdir.replace('mkt', market))

        for f in listfile:
            if day2csv_data(pathdir, f, targetDir, starttime=20050104, market=market):
                print(f, end='Done! ')
            else:
                print(f + 'FAILD!')
        else:
            print('The for ' + pathdir + ' to ' + targetDir + '  loop is over')
        print()
    else:
        result = day2csv_data(pathdir, market + single_code + '.day', targetDir=single_target_dir,
                              starttime=20050104, market=market)
        if result:
            print(result + ' file is saved!')
        else:
            print('File not found!')





