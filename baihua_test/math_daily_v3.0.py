import re
import random

class Quiz_generator(object):
    def __init__(self, type, max_quiz_per_page):
        self.type = type
        self.max_quiz_per_page = max_quiz_per_page
        self.elements = type.replace('?', '').find('=') + 1
        self.fill_in = False
        if type.find('?') >= 0:
            self.fill_in = True
        self.max = int(type[type.find('=') + 1 :type.find('[')])
        self.range = (int(type[type.find('[') + 1 :type.find(']')].split(',')[0]),
                      int(type[type.find('[') + 1:type.find(']')].split(',')[1]))

        self.quiz_per_page = []
        self.type_per_page = []

    def quiz_generate(self):
        for _ in range(self.max_quiz_per_page):
            self.quiz_per_page.append(self.random_quiz())
            self.type_per_page.append(self.type[:self.type.find('=') + 1])
        # print(quiz_per_page)
        # print(type_per_page)
        # [(['66', '36', '21'], 9), (['72', '11', '58'], 3), (['90', '36', '26'], 28), ...]
        # ['--=', '--=', '--=', '--=', '--=', '--=', '--=', '--=', '--=', '--=', '--=', ...]


    def random_quiz(self):
        while True:
            elements_list = []
            random_number = str(random.randint(self.range[0], self.range[1]))
            single_quiz = random_number
            elements_list.append(random_number)
            for i in range(self.elements - 1):
                single_quiz += self.type.replace('?', '')[i]
                random_number = str(random.randint(self.range[0], self.range[1]))
                single_quiz += random_number
                elements_list.append(random_number)

            if 0 < eval(single_quiz) <= self.max:
                return elements_list, eval(single_quiz)


def generate_one_day(date, page_per_day, file_name_surfix, types_per_page, max_quiz_per_page):
    for i in range(page_per_day):
        quiz_generator = Quiz_generator(types_per_page[i], max_quiz_per_page)
        quiz_generator.quiz_generate()
        print(quiz_generator.quiz_per_page)
        print(quiz_generator.type_per_page)
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

    try:
        # get max quizes per page:
        max_quiz_per_page = int(input('Pleas input max quiz per page? (default = 22 quiz)')) // 2 * 2
        if max_quiz_per_page > 22 or page_per_day <= 10:
            max_quiz_per_page = 22
    except ValueError:
        max_quiz_per_page = 22
    print(adv_date, page_per_day, max_quiz_per_page)

    # get file_name_surfix
    file_name_surfix = input("file name surfix:")
    if file_name_surfix != '':
        file_name_surfix = '_' + file_name_surfix

    return adv_date, page_per_day, file_name_surfix, max_quiz_per_page


def get_quiz_type_for_each_page(page):
    print('Please enter the %d page\'s quiz type' % page)
    print('type \'a+b+c+d=100[10, 99]\' stands for abcd all in [10,99] range and the result <=100')
    type = input('please give a type: (use enter to use previous or default(a+b=100)')
    if (page == 1 and type == '') or type.find('[') < 0 or type.find(']') < 0 or type.find(',') < 0 \
            or type.find('=') < 0:
        print('Use the default a+b=100[10,99]')
        return '+=100[10,99]'
    elif type == '':
        return 'previous'
    else:
        type1 = re.sub('[a-zA-Z!"#$%&\'().:;@\\^_`{|}~ \t\n\r\x0b\x0c]', '', type).replace(' ', '')
    return type1


def main():
    adv_date, page_per_day, file_name_surfix, max_quiz_per_page = get_genral_input()
    types_per_page = []
    for i in range(page_per_day):
        types_per_page.append(get_quiz_type_for_each_page(i + 1))
    today = 'sample'
    for i in range(adv_date):
        date = today + 'i'
        generate_one_day(date, page_per_day, file_name_surfix, types_per_page, max_quiz_per_page)
    pass


if __name__ == '__main__':
    main()
