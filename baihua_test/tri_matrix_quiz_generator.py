import random
import sys
import time
import turtle
from datetime import datetime

import keyboard
from PIL import Image


# color definition:  0 = green, 1 = yellow, 2 = yellow & green
# angel definition:  0 = no rotate, 1 = 90 degree rotate, 2 = 180 degree, 3 = 270 degree



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


def wait_keyin():
    while True:
        if keyboard.is_pressed('space'):
            break
        if keyboard.is_pressed('q'):
            sys.exit()

def draw_matrix():
    square = turtle.Turtle()
    square.hideturtle()
    square.pensize(1)
    square.speed(0)
    for i in range(len(matrix)):
        y = grid_y[i]
        step = abs(grid_x[1] - grid_x[0])
        for j in range(len(matrix[i])):
            if matrix[i][j] != 2:
                square.color('black', color[matrix[i][j]])
                square.penup()
                x = grid_x[j]
                square.setposition(x, y)
                square.setheading(0)
                square.pendown()
                square.begin_fill()
                for _ in range(4):
                    square.fd(step)
                    square.right(90)
                square.end_fill()
                square.penup()
            else:
                k = random.choice([0, 1])
                random.shuffle(dual_color)
                square.color('black', dual_color[0])
                square.penup()
                x = grid_x[j] + k * step
                step = abs(grid_x[1] - grid_x[0])
                square.setposition(x, y)
                square.setheading(0 + k * (-90))
                square.pendown()
                square.begin_fill()
                square.fd(step)
                square.right(90)
                square.fd(step)
                square.goto(x, y)
                square.end_fill()
                square.penup()
                # 2nd half
                square.color('black', dual_color[1])
                square.penup()
                square.setposition(x, y)
                square.setheading(-90 + k * (-90))
                square.pendown()
                square.begin_fill()
                square.fd(step)
                square.left(90)
                square.fd(step)
                square.goto(x, y)
                square.end_fill()
                square.penup()

    pass


def make_matrix():
    while True:
        matrix = []
        for _ in range(level):
            rows = []
            for _ in range(level):
                rows.append(random.choice([0, 1, 2]))
            matrix.append(rows)
        if sum(num.count(0) for num in matrix) <= level * level * 3 // 10 and \
            sum(num.count(1) for num in matrix) <= level * level * 3 // 10:
            # make sure the green and yellow pieces are less that 40% of the total pieces
            return matrix


def generate_symmetry(type):
    # 3 types, center, up/down, left/right
    pass


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

    for i in range(1, level):
        x = i * (grid_width // level) - grid_width // 2
        y = grid_height // 2 - i * (grid_height // level)
        grid_x.append(x)
        grid_y.append(y)
    grid_x.append(grid_width // 2)
    grid_y.append(grid_height // (-2))

    for i in range(len(grid_x) - 2):
        grid.penup()
        grid.goto(grid_x[i + 1], grid_y[0])
        grid.setheading(90)
        grid.pendown()
        grid.goto(grid_x[i + 1], grid_y[-1])

    for i in range(len(grid_y) - 2):
        grid.penup()
        grid.goto(grid_x[0], grid_y[i + 1])
        grid.setheading(0)
        grid.pendown()
        grid.goto(grid_x[-1], grid_y[i + 1])

    return grid_x, grid_y


time_to_remember = 30
canvas_width = 600
canvas_height = 600
color = ['green', 'yellow']
dual_color = color.copy()

today = datetime.now().date().strftime('%Y_%m_%d')
folder = 'e:\\einom\\Documents\\___SOPHIA____\\--Sophia K2 Folder\\BAIHUA_LOGICS\\'

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

level = 4

# level has 3x3 & 4X4
k = 0

while True:

    grid_x, grid_y = draw_grid()
    matrix = make_matrix()
    draw_matrix()

    write_info('pleas press \'space\' to continue!')

    turtle.getscreen().getcanvas().postscript(file='tmp.ps')

    img = Image.open('tmp.ps')
    try:
        img.save(folder + 'tri_matrix_' + today + '--' + '0' * (3 - len(str(k))) + str(k) + '.jpg')
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



    wait_keyin()

    wn.clear()

    k += 1