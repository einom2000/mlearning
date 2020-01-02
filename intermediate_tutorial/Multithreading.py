import random
import threading

import pygame


def f():
    x = 80
    y = 80
    xd = 1
    yd = 1
    while True:
        screen.fill((0, 0, 255))
        pygame.draw.circle(screen, (255, 0, 0, 255), (x, y), 80)
        pygame.display.flip()
        x += xd
        y += yd
        if x == (500 - 80) or x == 80:
            xd = -xd
        if y == (400 - 80) or y == 80:
            yd = -yd
        pygame.time.delay(10)


def g():
    x = random.choice([120, 80, 40])
    y = random.choice([120, 80, 40])
    xd = 2
    yd = 2
    while True:
        pygame.draw.circle(screen, (0, 255, 0, 255), (x, y), 40)
        x += xd
        y += yd
        if x == (500 - 40) or x == 40:
            xd = -xd
        if y == (400 - 40) or y == 40:
            yd = -yd
        pygame.time.delay(10)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    t = threading.Thread(target=f)
    t1 = threading.Thread(target=g)
    t2 = threading.Thread(target=g)
    t.setDaemon(True)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t.start()
    t1.start()
    t2.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.delay(100)

quit()
