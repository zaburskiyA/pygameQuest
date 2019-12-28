import pygame

running = True
pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
v = 100
screen.fill(pygame.Color('blue'))
pygame.display.flip()
fps = 60
flag = False
screen.fill((0, 0, 255))


def draw():
    global x_pos
    screen.fill((0, 0, 255))
    pygame.draw.circle(screen, (pygame.Color('yellow')), position, int(x_pos))
    x_pos += v / fps
    clock.tick(fps)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag = True
            x_pos = 1
            position = event.pos

    if flag:
        draw()
    pygame.display.flip()
