import pygame
from player import Player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 300))

player = Player("music")

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill((0, 0, 0))

    text = font.render("Track: " + player.tracks[player.index], True, (255, 255, 255))
    screen.blit(text, (50, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            if event.key == pygame.K_s:
                player.stop()
            if event.key == pygame.K_n:
                player.next()
            if event.key == pygame.K_b:
                player.prev()
            if event.key == pygame.K_q:
                running = False

    pygame.display.update()

pygame.quit()