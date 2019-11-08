import turtle
import random


def generate_list(level):
    colors = ['red', 'green', 'blue', 'white', 'brown', 'pink', 'black', 'orange']
    color_list = []
    if level == 1:
        random.shuffle(colors)
        for color in colors:
            color_list.append(color)
            color_list.append(color)
    if level == 2:
        color_list = colors + colors
        random.shuffle(color_list)
    matrix = []
    for i in range(4):
        tmp = []
        for j in range(4):
            tmp.append(color_list[i * 4 + j])
        matrix.append(tmp)
    return matrix


def get_level():
    level = input('please input the dificulties [1(easy) or 2(hard)]:')
    try:
        level = int(level)
        if level > 2:
            level = 2
        if level < 1:
            level = 1
    except ValueError:
        level = 1
    return level


level = get_level()
matrix = generate_list(level)
wn
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")

wn.setup(810, 810)

grid = turtle.Turtle()
grid.pensize(1)
grid.color('black')
grid.speed(10)
grid.penup()
grid.setposition(-400, 400)
grid.pendown()
grid.setheading(0)
for _ in range(4):
    grid.fd(800)
    grid.right(90)

print('done')

wn.exitonclick()






