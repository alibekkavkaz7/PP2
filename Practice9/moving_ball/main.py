import pygame
from ball import Ball

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))

ball = Ball(300, 200)

running = True
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ball.move(keys, width, height)
    ball.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()