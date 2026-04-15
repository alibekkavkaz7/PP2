import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((500, 500))
center = (250, 250)

bg = pygame.image.load("images/mickeyclock.jpeg")
bg = pygame.transform.scale(bg, (500, 500))

hand_img = pygame.image.load("images/hand.png")
clock_obj = MickeyClock(hand_img)

clock = pygame.time.Clock()

running = True
while running:
    screen.blit(bg, (0, 0))

    clock_obj.draw(screen, center)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(1)

pygame.quit()