import random
import turtle
from datetime import datetime, timedelta

from PIL import Image


def draw_circle(x, y, radius, color):
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color(color)
    t.setx(x)
    t.sety(y - radius)
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()


def draw_square(x, y, radius, color):
    rd_dgr = random.choice(turn_degrees)
    print(rd_dgr)
    edge = int(radius * 1.414)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color(color)
    t.setx(x - edge // 2)
    t.sety(y + edge // 2)
    t.pendown()
    t.setheading(270 + rd_dgr)
    t.begin_fill()
    for _ in range(4):
        t.fd(edge)
        t.left(90)
    t.end_fill()


def draw_triangle(x, y, radius, color):
    rd_dgr = random.choice(turn_degrees)
    edge = int(radius * 1.732)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color(color)
    t.setx(x)
    t.sety(y + radius)
    t.pendown()
    t.setheading(270 + rd_dgr)
    t.begin_fill()
    for _ in range(3):
        t.fd(edge)
        t.left(120)
    t.end_fill()


def draw_star(x, y, radius, color):
    rd_dgr = random.choice(turn_degrees)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color(color)
    t.setx(x - radius // 2)
    t.sety(y)
    t.pendown()
    t.setheading(0 + rd_dgr)
    t.begin_fill()
    for _ in range(5):
        t.fd(radius * 1.5)
        t.right(144)
    t.end_fill()


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
        y = grid_height // 2 - grid_height // 4 - i * grid_height // 2
        for j in range(4):
            x = grid_width // 8 + j * grid_width // 4 - grid_width // 2
            position.append((x, y))

    return position


def draw_sizes(position):
    random.shuffle(sizes)
    methods = [draw_square, draw_circle, draw_triangle, draw_star]
    method = random.choice(methods)
    for pos in position:
        print(pos)
        method(pos[0], pos[1], sizes[position.index(pos)], colors[position.index(pos)])
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


time_to_remember = 30
canvas_width = 1000
canvas_height = 600
sizes = [10 + 14 * x for x in range(8)]
colors = ['red', 'green', 'blue', 'brown', 'black', 'gray', 'pink', 'orange']
style = ('Courier', 10, 'bold')
turn_degrees = [-60, -30, 0, 30, 60]

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")
wn.setup(canvas_width, canvas_height)
grid_width = canvas_width - 100
grid_height = canvas_height - 100
circles = []

for k in range(1, 4):

    position = draw_grid()
    draw_sizes(position)

    write_info(today + '  please press \'space\' to new one!')

    while True:

        # if keyboard.is_pressed('space'):

        turtle.getscreen().getcanvas().postscript(file='tmp.ps', colormode='color')

        img = Image.open('tmp.ps')
        try:
            img.save(folder + 'size_squence_' + today + '--' + '0' * (3 - len(str(k))) + str(k) + '.jpg')
            break
        except FileNotFoundError:
            pass
            break
        # if keyboard.is_pressed('q'):
        #     sys.exit()

    wn.clear()

