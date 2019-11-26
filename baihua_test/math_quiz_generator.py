from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor
from docx.shared import Inches

from datetime import datetime
import random

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
    if field[1] - field[0] <= quiz_number:
        field[1] = quiz_number + field[0]
    subjs = random.sample(range(field[0], field[1] + 1), quiz_number)
    quizs = []
    for subj in subjs:
        tmp = [subj, random.choice(obj)]
        random.shuffle(tmp)
        quizs.append(tmp)
    quiz_table = []
    for i in range(0, len(quizs), 2):
        quiz_table.append((str(quizs[i][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i][1]) + ' =',
                           str(quizs[i + 1][0]) + ' ' + calc_dic[calc] + ' ' + str(quizs[i + 1][1]) + ' ='))
    return quiz_table


def create_doc(quiz_table, file_number):
    document = Document()
    number = obj[0]  # Subtraction multiplication division
    title1 = datetime.now().date().strftime('%Y/%m/%d') + ' -- '
    title2 = calc.upper()
    title3 = ' of number '
    title4 = str(number) + '\n'
    title5 = trans(calc)

    # title creation
    p = document.add_heading(level=0)
    wp = p.add_run(title1)
    wp.font.size = Pt(25)
    wp.font.bold = True
    wp.font.color.rgb = RGBColor(0, 0, 0)
    wp = p.add_run(title2)
    wp.font.size = Pt(30)
    wp.font.color.rgb = RGBColor(255, 0, 0)
    wp = p.add_run(title3)
    wp.font.size = Pt(25)
    wp.font.bold = True
    wp.font.color.rgb = RGBColor(0, 0, 0)
    wp = p.add_run(title4)
    wp.font.size = Pt(30)
    wp.font.color.rgb = RGBColor(255, 0, 0)

    wp = p.add_run('关于数字 ')
    wp.font.size = Pt(25)
    wp.font.bold = True
    wp.font.color.rgb = RGBColor(0, 0, 0)
    wp = p.add_run(str(number))
    wp.font.size = Pt(30)
    wp.font.color.rgb = RGBColor(255, 0, 0)
    wp = p.add_run(' 的')
    wp.font.size = Pt(25)
    wp.font.bold = True
    wp.font.color.rgb = RGBColor(0, 0, 0)
    wp = p.add_run(title5)
    wp.font.size = Pt(30)
    wp.font.color.rgb = RGBColor(255, 0, 0)
    wp = p.add_run('练习')
    wp.font.size = Pt(25)
    wp.font.color.rgb = RGBColor(0, 0, 0)

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

    document.save('math_quiz' + '0' * (3 - len(str(file_number))) + str(file_number) + '.docx')


obj = [2,]
quiz_number = 10
field = [0, 12]
calc = 'addition'


for i in range(0, 3):
    quiz_table = quiz_create(field, obj, calc, quiz_number)
    create_doc(quiz_table, i)
