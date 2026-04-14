import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((500, 500))
center = (250, 250)

image = pygame.image.load("images/mickey_hand.png")
clock_obj = MickeyClock(image)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    clock_obj.draw(screen, center)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(1)

pygame.quit()