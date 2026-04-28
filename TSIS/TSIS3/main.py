import pygame, sys, random
from racer import *
from ui import *
from persistence import *

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# загрузка ресурсов (ОДИН РАЗ → нет лагов)
player_img = pygame.transform.scale(pygame.image.load("assets/player.png"), (60,100))
enemy_img = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (60,100))
background = pygame.image.load("assets/road.png")

settings = load_settings()

def run_game():
    player = Player(player_img)
    enemies = []
    oils = []
    powers = []

    speed = 6
    distance = 0
    coins = 0

    running = True
    while running:
        clock.tick(60)
        screen.blit(background,(0,0))

        distance += 1
        score = coins + distance//10

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT: player.move("left")
                if e.key == pygame.K_RIGHT: player.move("right")

        # спавн без появления на игроке
        if random.randint(1,40)==1:
            enemies.append(Enemy(enemy_img, speed))

        if random.randint(1,60)==1:
            oils.append(Oil(speed))

        if random.randint(1,120)==1:
            powers.append(PowerUp(speed))

        # обновление
        for obj in enemies + oils + powers:
            obj.update()

        # коллизии
        for en in enemies:
            if player.rect.colliderect(en.rect):
                if player.shield:
                    player.shield = False
                    enemies.remove(en)
                else:
                    return score, distance

        for p in powers:
            if player.rect.colliderect(p.rect):
                if p.type == "shield":
                    player.shield = True
                if p.type == "nitro":
                    speed += 3
                powers.remove(p)

        # отрисовка
        screen.blit(player.image, player.rect)

        for en in enemies:
            screen.blit(en.image, en.rect)

        for o in oils:
            pygame.draw.circle(screen, (0,0,0), o.rect.center, 20)

        for p in powers:
            color = (0,255,0) if p.type=="shield" else (0,0,255)
            pygame.draw.circle(screen, color, p.rect.center, 15)

        draw_text(screen, f"Score: {score}", 20, 80, 30)
        draw_text(screen, f"Distance: {distance}", 20, 350, 30)

        pygame.display.update()

while True:
    choice = main_menu(screen)

    if choice == "play":
        score, dist = run_game()
        save_score("Player", score, dist)

    elif choice == "leaderboard":
        leaderboard_screen(screen, load_scores())

    elif choice == "settings":
        settings = settings_screen(screen, settings)
        save_settings(settings)

    elif choice == "quit":
        pygame.quit()
        sys.exit()