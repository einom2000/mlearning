import random
from datetime import datetime, timedelta

from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor


# translation function
def trans(calc):
    tmp = ''
    if calc == 'division':
        tmp = '除法'
    elif calc == 'subtraction':
        tmp = '减法'
    elif calc == 'multiplication':
        tmp = '乘法'
    else:
        tmp = '加法'
    return tmp


# create quiz list
def quiz_create(field, obj, calc, quiz_number):
    calc_dic = {'addition': '+',
                'subtraction': '-',
                'multiplication': 'x',
                'division': '÷'}
    if field[1] - field[0] + 1 < quiz_number:
        length = field[1] - field[0] + 1
    else:
        length = quiz_number
    length = length // 2 * 2
    subjs = random.sample(range(field[0], field[1] + 1), length)
    quizs = []
    for subj in subjs:
        tmp = [subj, random.choice(obj)]
        random.shuffle(tmp)
        quizs.append(tmp)
    quiz_table = []
    quiz_table1 = []
    for i in range(0, len(quizs), 2):
        quiz_table.append((str(quizs[i][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i][1]) + ' =',
                           str(quizs[i + 1][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i + 1][1]) + ' ='))
    if quiz_number > length:
        length1 = quiz_number - length
        if length1 + length > max_quizs_per_page:
            length1 = max_quizs_per_page - length
        subjs = random.sample(range(field[0], field[1] + 1), length1)
        quizs = []
        for subj in subjs:
            tmp = [subj, random.choice(obj)]
            random.shuffle(tmp)
            quizs.append(tmp)
        for i in range(0, len(quizs), 2):
            quiz_table1.append((str(quizs[i][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i][1]) + ' =',
                               str(quizs[i + 1][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i + 1][1]) + ' ='))
    return quiz_table + quiz_table1


def create_doc(i):
    document = Document()
    number = ''
    for k in obj:
        number += str(k) + ','
    number = number[:-1]

    title1 = target_date + ' -- '
    title2 = calc.upper()
    title3 = ' of number '
    title4 = str(number) + '\n'
    title5 = trans(calc)

    for page in range(i):
        # title creation
        p = document.add_heading(level=0)
        wp = p.add_run(title1)
        wp.font.size = Pt(20)
        wp.font.bold = True
        wp.font.color.rgb = RGBColor(0, 0, 0)
        wp = p.add_run(title2)
        wp.font.size = Pt(20)
        wp.font.color.rgb = RGBColor(255, 0, 0)
        wp = p.add_run(title3)
        wp.font.size = Pt(20)
        wp.font.bold = True
        wp.font.color.rgb = RGBColor(0, 0, 0)
        wp = p.add_run(title4)
        wp.font.size = Pt(20)
        wp.font.color.rgb = RGBColor(255, 0, 0)

        wp = p.add_run('关于数字 ')
        wp.font.name = '#simSong'
        wp.font.size = Pt(20)
        wp.font.bold = True
        wp.font.color.rgb = RGBColor(0, 0, 0)
        wp = p.add_run(str(number))
        wp.font.size = Pt(20)
        wp.font.color.rgb = RGBColor(255, 0, 0)
        wp = p.add_run(' 的')
        wp.font.size = Pt(20)
        wp.font.bold = True
        wp.font.color.rgb = RGBColor(0, 0, 0)
        wp = p.add_run(title5)
        wp.font.size = Pt(20)
        wp.font.color.rgb = RGBColor(255, 0, 0)
        wp = p.add_run('练习 -- 第 ' + str(page + 1) + ' 页')
        wp.font.size = Pt(20)
        wp.font.bold = True
        wp.font.color.rgb = RGBColor(0, 0, 0)


        quiz_table = quiz_create(field, obj, calc, quiz_number)
        table = document.add_table(rows=1, cols=2)

        for q1, q2 in quiz_table:
            row_cells = table.add_row().cells
            row_cells[0].text = q1
            row_cells[1].text = q2

        for row in table.rows:
            for cell in row.cells:
                paragraphs = cell.paragraphs
                for paragraph in paragraphs:
                    for run in paragraph.runs:
                        font = run.font
                        font.size = Pt(30)
        if page < i -1:
            document.add_page_break()
    try:
        document.save('e:\\einom\Documents\\___SOPHIA____\\--Sophia K2 Folder\\MATH_PRACTICE\\math_quiz' + '_' + \
                      target_date + '.docx')
    except FileNotFoundError:
        document.save('temp.docx')


adv_day = int(input('any advanced day? (0=no)'))
target_date = (datetime.now() + timedelta(days=adv_day)).date().strftime('%Y_%m_%d')

obj = [3, 2]          # 2 to plus the other number
quiz_number = 16    # quiz per page in 2 columns
field = [0, 10]     # 0 ~ 12 number to plus
calc = 'addition'
max_quizs_per_page = 20

create_doc(3)
