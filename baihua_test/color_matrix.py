import turtle
import random


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
            print(x, y)
            square.setposition(x, y)
            square.setheading(0)
            square.pendown()
            square.begin_fill()
            for _ in range(4):
                square.fd(step)
                square.right(90)
            square.end_fill()
            square.penup()





level = get_level()
matrix = generate_list(level)
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("color_matrix")
canvas_width = 1000
canvas_height = 1000
wn.setup(canvas_width, canvas_height)
grid_width = canvas_width - 200
grid_height = canvas_height - 200


grid_x, grid_y = draw_grid()
draw_matrix(matrix, grid_x, grid_y)

turtle.getscreen().getcanvas().postscript(file='11.ps')
wn.exitonclick()






