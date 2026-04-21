import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

snake = [(100,100)]
dx, dy = CELL, 0

# еда как класс (есть value и таймер)
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            if (x,y) not in snake:
                break

        self.pos = (x,y)

        # разный "вес" еды
        self.value = random.choice([1,2,3])

        # время появления (для исчезновения)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        # цвет зависит от value
        colors = {
            1: (255,0,0),
            2: (255,165,0),
            3: (255,255,0)
        }
        pygame.draw.rect(screen, colors[self.value], (*self.pos, CELL, CELL))

food = Food()

score = 0
level = 1

move_delay = 150
last_move = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 25)

while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление
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

    # движение по таймеру
    if now - last_move > move_delay:
        last_move = now

        new_x = snake[0][0] + dx
        new_y = snake[0][1] + dy

        # не выходим за границы
        if not (0 <= new_x < WIDTH and 0 <= new_y < HEIGHT):
            new_x, new_y = snake[0]

        head = (new_x, new_y)

        # сам в себя
        if head in snake:
            break

        snake.insert(0, head)

        # если еда "протухла" (5 сек)
        if now - food.spawn_time > 5000:
            food.respawn()

        # съели еду
        if head == food.pos:
            score += food.value
            food.respawn()

            # уровень
            if score % 5 == 0:
                level += 1
                move_delay = max(60, move_delay - 10)

        else:
            snake.pop()

    # рисуем
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    food.draw()

    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10,10))

    pygame.display.update()

# game over
screen.fill(WHITE)
game_over = font.render("Game Over", True, RED)
screen.blit(game_over, (140,180))
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()