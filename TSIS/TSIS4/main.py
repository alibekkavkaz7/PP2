import pygame
import sys
import json
from game import *
from db import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

init_db()

username = input("Enter username: ")

best_score = get_best(username)

snake = [(100,100)]
dx, dy = CELL, 0

food = Food()
poison = Poison()
power = None

score = 0
level = 1
move_delay = 150
last_move = pygame.time.get_ticks()

active_power = None
power_end = 0

while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    now = pygame.time.get_ticks()

    # движение
    if now - last_move > move_delay:
        last_move = now

        head = (snake[0][0] + dx, snake[0][1] + dy)

        if head in snake:
            break

        snake.insert(0, head)

        # обычная еда
        if head == food.pos:
            score += food.value
            food.spawn()

        # яд
        elif head == poison.pos:
            snake = snake[:-2]
            poison.spawn()
            if len(snake) <= 1:
                break

        # power-up
        elif power and head == power.pos:
            active_power = power.type
            power_end = now + 5000
            power = None

        else:
            snake.pop()

    # power-up таймер
    if active_power and now > power_end:
        active_power = None

    # спавн power-up
    if not power and random.random() < 0.01:
        power = PowerUp()

    # уровни
    if score % 5 == 0 and score != 0:
        level += 1
        move_delay = max(60, move_delay - 10)

    # отрисовка
    screen.fill(BLACK)

    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, CELL, CELL))

    food.draw(screen)
    poison.draw(screen)

    if power:
        power.draw(screen)

    text = font.render(f"Score:{score} Level:{level} Best:{best_score}", True, WHITE)
    screen.blit(text, (10,10))

    pygame.display.update()

# сохраняем результат
save_score(username, score, level)

pygame.quit()