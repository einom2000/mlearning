import turtle
import random
from PIL import Image
import keyboard
import sys
import time
import argparse
from datetime import datetime
import tkinter as tk


def generate_list(level):
    colors = ['red', 'green', 'blue', 'white', 'sky blue', 'pink', 'black', 'orange']
    color_list = []
    if level == 1:
        random.shuffle(colors)
        for color in colors:
            color_list.append(color)
            color_list.append(color)
    if level == 2:
        color_list = colors + colors
        random.shuffle(color_list)
    if level > 2 and level != 999:
        cover_pieces = 16 - level
        color_list = colors + colors
        random.shuffle(color_list)
        if cover_pieces > 14:
            cover_pieces = 14
        index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        random.shuffle(index)
        for i in range(0, cover_pieces - 2):  # because there are 2 blocks already in white
            if color_list[index[i]] == 'white':
                index.pop(i)
            color_list[index[i]] = 'white'
    if level == 999:
        color_list = ['black', 'white'] * 8
        random.shuffle(color_list)

    matrix = []
    for i in range(4):
        tmp = []
        for j in range(4):
            tmp.append(color_list[i * 4 + j])
        matrix.append(tmp)

    is_rotate = random.choice([True, False])
    if is_rotate:
        matrix = list(zip(*matrix))

    return matrix


def calc_level(e1):
    global level
    level = e1.get()
    try:
        level = int(level)
        if level > 14 and level != 999:
            level = 2   # show 14 pieces == level 2
        elif level <= 1:
            level = 1
        elif level > 14:
            level = 999
    except ValueError:
        level = 666
    print('level = ' + str(level))

def get_level():
    master = tk.Tk()
    tk.Label(master, text="please input a level to play").grid(row=0)
    tk.Label(master, text="999 FOR B/W, 14+ FOR LEVEL2, 1 FOR LEVEL 1, 2~14 FOR COLORED PIECES").grid(row=2)
    tk.Label(master, text='PLS INPUT NUMBER ONLY').grid(row=3)
    e1 = tk.Entry(master)
    e1.grid(row=0, column=1)
    e1.insert(tk.END, '999')

    tk.Button(master, text='GO', command=lambda: calc_level(e1)).grid(row=4, column=0, sticky=tk.W, pady=4)
    print(level)
    if level != 666 and level != 0:
        print('destroy window!')
        master.destroy()
    elif level == 666:
        warning_msg = 'WRONG INPUT!, PLS INPUT AGAIN!'
    else:
        master.mainloop()
    return level


def draw_grid():
    grid_x = [grid_width // (-2)]
    grid_y = [grid_height // 2]
    grid = turtle.Turtle()
    grid.hideturtle()
    grid.pensize(1)
    grid.color('black')
    grid.speed(0)
    grid.penup()
    grid.setposition(grid_width // (-2), grid_height // 2)
    grid.pendown()
    grid.setheading(0)
    for _ in range(4):
        grid.fd(grid_width)
        grid.right(90)
    grid.penup()

    for i in range(1, 4):
        x = i * (grid_width // 4) - grid_width // 2
        y = grid_height // 2 - i * (grid_height // 4)
        grid_x.append(x)
        grid_y.append(y)
    grid_x.append(grid_width // 2)
    grid_y.append(grid_height // (-2))

    return grid_x, grid_y


def draw_matrix(matrix, grid_x, grid_y):
    square = turtle.Turtle()
    square.hideturtle()
    square.pensize(1)
    square.speed(0)
    for i in range(len(matrix)):
        y = grid_y[i]
        for j in range(len(matrix[i])):
            square.color('black', matrix[i][j])
            square.penup()
            x = grid_x[j]
            step = abs(grid_x[1] - grid_x[0])
            square.setposition(x, y)
            square.setheading(0)
            square.pendown()
            square.begin_fill()
            for _ in range(4):
                square.fd(step)
                square.right(90)
            square.end_fill()
            square.penup()


def write_info(text):
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(0, (canvas_height // 2 - 50) * (-1))
    turtle.pendown()
    turtle.color('black')
    turtle.write(text, font=style, align='center')
    turtle.penup()
    turtle.goto(0, (canvas_height // 2 - 20) * (-1))
    turtle.pendown()
    turtle.write('or press \'q\' to quit', font=style, align='center')


def write_info2():
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.write('pleas press \'space\' to have show it again!', font=style, align='center')
    turtle.penup()
    turtle.goto(0, -100)
    turtle.pendown()
    turtle.write('or press \'q\' to quit', font=style, align='center')
    turtle.penup()


def wait_keyin():
    while True:
        if keyboard.is_pressed('space'):
            break
        if keyboard.is_pressed('q'):
            sys.exit()


time_to_remember = 30
canvas_width = 600
canvas_height = 600

today = datetime.now().date().strftime('%Y_%m_%d')
folder = 'e:\\einom\\Documents\\___SOPHIA____\\--Sophia K2 Folder\\BAIHUA_LOGICS\\'

level = 0
level = get_level()


wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")
wn.setup(canvas_width, canvas_height)
grid_width = canvas_width - 200
grid_height = canvas_height - 200

ct_pen = turtle.Turtle()
ct_pen.hideturtle()
ct_pen.pensize(3)
ct_pen.color('red')
ct_pen.speed(0)
ct_style = ('Courier', 30, 'bold')
style = ('Courier', 10, 'bold')
k = 1


while True:

    matrix = generate_list(level)

    grid_x, grid_y = draw_grid()
    draw_matrix(matrix, grid_x, grid_y)

    write_info('pleas press \'space\' to hide!')

    turtle.getscreen().getcanvas().postscript(file='tmp.ps')

    img = Image.open('tmp.ps')
    try:
        img.save(folder + 'color_4x4_matrix_' + today + '--' + '0' * (3 - len(str(k))) + str(k) + '.jpg')
    except FileNotFoundError:
        pass

    ct = time.time()
    last_dt = 0

    while True:

        dt = int(time.time() - ct)
        if dt - last_dt > 0:
            ct_pen.clear()
            ct_pen.penup()
            ct_pen.setposition(0, (canvas_height // 2 - 70))
            ct_pen.pendown()
            # ct_pen.write(str(time_to_remember - dt), font=ct_style, align='center')
            last_dt = dt
        if last_dt == time_to_remember:
            break
        if keyboard.is_pressed('space'):
            break
        if keyboard.is_pressed('q'):
            sys.exit()

    wn.clear()

    write_info2()

    wait_keyin()

    draw_matrix(matrix, grid_x, grid_y)
    write_info('pleas press \'space\' to have a new pattern!')

    wait_keyin()

    wn.clear()

    k += 1






