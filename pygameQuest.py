import pygame


running = True
pygame.init()
screen = pygame.display.set_mode((1000, 700))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
