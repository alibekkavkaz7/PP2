import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

# Snake initial state
snake = [(100,100)]
dx, dy = CELL, 0

# Generate food not on snake
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x,y) not in snake:
            return (x,y)

food = generate_food()

# Game stats
score = 0
level = 1

# Movement timing (separates FPS from snake speed)
move_delay = 150
last_move = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 25)

# Game loop
while True:

    # High FPS for responsive input
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle direction changes
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

    # Move snake based on timer
    if now - last_move > move_delay:
        last_move = now

        new_x = snake[0][0] + dx
        new_y = snake[0][1] + dy

        # Border check (snake cannot leave screen)
        if not (0 <= new_x < WIDTH and 0 <= new_y < HEIGHT):
            new_x, new_y = snake[0]

        head = (new_x, new_y)

        # Self collision
        if head in snake:
            break

        snake.insert(0, head)

        # Food collision
        if head == food:
            score += 1
            food = generate_food()

            # Level system
            if score % 4 == 0:
                level += 1
                move_delay = max(60, move_delay - 10)
        else:
            snake.pop()

    # Drawing
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10,10))

    pygame.display.update()

# Game over screen
screen.fill(WHITE)
game_over = font.render("Game Over", True, RED)
screen.blit(game_over, (140,180))
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()