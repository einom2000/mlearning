import math
import random
import turtle
from datetime import datetime, timedelta

from PIL import Image


def draw_glass(x, y, level, color):
    t = turtle.Turtle()
    level = level / 100
    fd_1 = int(level * 150)
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color(color)
    t.setx(x)
    t.sety(y)
    t.pendown()
    # draw water
    t.begin_fill()
    t.fd(50)
    t.left(85)
    t.fd(fd_1)
    t.left(95)
    t.fd(50 + 2 * math.sin(math.radians(5)) * fd_1)
    t.left(95)
    t.fd(fd_1)
    t.end_fill()
    #.draw_cups
    t.left(85)
    t.fd(50)
    t.left(85)
    t.fd(150)
    t.left(95)
    t.fd(50 + 2 * math.sin(math.radians(5)) * 150)
    t.left(95)
    t.fd(150)

def draw_grid():
    grid = turtle.Turtle()
    grid.hideturtle()
    grid.pensize(1)
    grid.color('black')
    grid.speed(0)
    grid.penup()
    grid.setposition(grid_width // (-2), grid_height // 2)
    grid.pendown()
    grid.setheading(0)
    for _ in range(2):
        grid.fd(grid_width)
        grid.right(90)
        grid.fd(grid_height)
        grid.right(90)
    grid.penup()

    position = []

    for i in range(2):
        y = grid_height // 2 - grid_height // 4 - i * grid_height // 2 - grid_height // 8
        for j in range(4):
            x = grid_width // 8 + j * grid_width // 4 - grid_width // 2
            position.append((x, y))

    return position


def draw_sizes(position):
    random.shuffle(levels)
    for pos in position:
        print(pos)
        draw_glass(pos[0], pos[1], levels[position.index(pos)], colors[position.index(pos)])
        print(pos)


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


adv_day = int(input('any advanced day? (0=no)'))
today = (datetime.now() + timedelta(days=adv_day)).date().strftime('%Y_%m_%d')
folder = 'e:\\einom\\Documents\\___SOPHIA____\\--Sophia K2 Folder\\BAIHUA_LOGICS\\'

canvas_width = 1000
canvas_height = 600
levels = [0, 15, 30, 50, 65, 80, 100, 95]
colors = ['red', 'green', 'blue', 'brown', 'black', 'gray', 'pink', 'orange']
style = ('Courier', 10, 'bold')

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")
wn.setup(canvas_width, canvas_height)
grid_width = canvas_width - 100
grid_height = canvas_height - 100

for k in range(1, 4):

    position = draw_grid()
    draw_sizes(position)

    write_info(today + '  please press \'space\' to new one!')

    while True:

        # if keyboard.is_pressed('space'):

        turtle.getscreen().getcanvas().postscript(file='tmp.ps', colormode='color')

        img = Image.open('tmp.ps')
        try:
            img.save(folder + 'volume_squence_' + today + '--' + '0' * (3 - len(str(k))) + str(k) + '.jpg')
            break
        except FileNotFoundError:
            pass
            break
        # if keyboard.is_pressed('q'):
        #     sys.exit()

    wn.clear()

