import random
import re
from datetime import datetime, timedelta

from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor


class Normal_addition_multiplications(object):
    def __init__(self, type):
        self.type = type
        self.elements = type.find('=') + 1
    # a + b + c + d.... = ? or a * b * c ....= ?
    pass

class Filling_in_addition_muiltiplications(object):
    # a + ? + c = d or a * ? * c ....= d
    pass

class Normal_subtraction_division(object):
    # a - b - c + d.... = ? or a / b / c ....= ?
    pass

class Filling_in_subtraction_division(object):
    # a - ? - c  = d or a / ? ....= d
    pass

class All_kinds(object):
    pass


def generate_one_day(date, page_per_day, file_name_surfix, types_per_page):
    for i in range(page_per_day):
        type = types_per_page[i][0]
        if type == '+':
            add = Normal_addition_multiplications(types_per_page[i])

    pass


def get_genral_input():
    # get the dates to print
    try:
        adv_date = int(input('How many days from now? (default = 1(today), max = 30days)')) + 0
        if adv_date > 30 or adv_date <= 0:
            adv_date = 1
    except ValueError:
        adv_date = 1

    # get how many pages per day:
    try:
        page_per_day = int(input('How many pages per day? (default = 3 pages, max = 5 pages)'))
        if page_per_day >5 or page_per_day <= 0:
            page_per_day = 1
    except ValueError:
        page_per_day = 3
    print(adv_date, page_per_day)

    # get file_name_surfix
    file_name_surfix = input("file name surfix:")
    if file_name_surfix != '':
        file_name_surfix = '_' + file_name_surfix

    return adv_date, page_per_day, file_name_surfix


def get_quiz_type_for_each_page(page):
    print('Please enter the %d page\'s quiz type' % page)
    print('type \'a+b+c+d=100[10, 99]\' stands for abcd all in [10,99] range and the result <=100')
    type = input('please give a type: (use enter to use previous or default(a+b=100)')
    if (page == 1 and type == '') or type.find('[') < 0 or type.find(']') < 0 or type.find(',') < 0 or :
        print('Use the default a+b=100[10,99]')
        return 'a+b=100[10,99]'
    elif type == '':
        return 'previous'
    else:
        type1 = re.sub('[a-zA-Z!"#$%&\'().:;@\\^_`{|}~ \t\n\r\x0b\x0c]', '', type).replace(' ', '')
    return type1


def main():
    adv_date, page_per_day, file_name_surfix = get_genral_input()
    types_per_page = []
    for i in range(page_per_day):
        types_per_page.append(get_quiz_type_for_each_page(i + 1))
    today = 'sample'
    for i in range(adv_date):
        date = today + i
        generate_one_day(date, page_per_day, file_name_surfix, types_per_page)
    pass


if __name__ == '__main__':
    main()
