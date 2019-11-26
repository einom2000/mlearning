import turtle
import random
import keyboard
import sys
from datetime import datetime


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
        y = grid_height // 2 - grid_height // 4 - i * grid_height // 2 - trimy
        for j in range(4):
            x = grid_width // 8 + j * grid_width // 4 - grid_width // 2 - trimx
            position.append((x, y))

    return position


def draw_sizes(position):
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.color('red')
    random.shuffle(sizes)

    for pos in position:
        t.setx(pos[0])
        t.sety(pos[1])
        t.pendown()
        size = sizes[position.index(pos)]
        color = colors[position.index(pos)]
        t.color(color)
        t.write("★", font=("Arial", size, "normal"))  # ★
        t.penup()


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


today = datetime.now().date().strftime('%Y_%m_%d')
folder = 'e:\\einom\\Documents\\___SOPHIA____\\--Sophia K2 Folder\\BAIHUA_LOGICS\\'


time_to_remember = 30
canvas_width = 1000
canvas_height = 600
trimx = 80
trimy = 100
sizes = [35, 50, 65, 80, 95, 110, 125, 140]
colors = ['red', 'green', 'blue', 'brown', 'black', 'gray', 'pink', 'orange']
style = ('Courier', 10, 'bold')

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")
wn.setup(canvas_width, canvas_height)
grid_width = canvas_width - 100
grid_height = canvas_height - 100



while True:

    position = draw_grid()
    draw_sizes(position)

    write_info('pleas press \'space\' to new one!')

    while True:

        if keyboard.is_pressed('space'):
            break
        if keyboard.is_pressed('q'):
            sys.exit()

    wn.clear()

