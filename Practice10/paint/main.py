import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

color = BLACK
radius = 5

mode = "draw"
start_pos = None

# Canvas
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Font for menu
font = pygame.font.SysFont("Arial", 18)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Modes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                mode = "draw"
            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_e:
                mode = "eraser"

            # Colors
            if event.key == pygame.K_1:
                color = RED
            if event.key == pygame.K_2:
                color = GREEN
            if event.key == pygame.K_3:
                color = BLUE
            if event.key == pygame.K_4:
                color = BLACK

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos

            if mode == "rect":
                rect = pygame.Rect(start_pos[0], start_pos[1],
                                   end_pos[0]-start_pos[0],
                                   end_pos[1]-start_pos[1])
                pygame.draw.rect(canvas, color, rect, 2)

            if mode == "circle":
                radius_circle = int(((end_pos[0]-start_pos[0])**2 +
                                     (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, radius_circle, 2)

    # Drawing
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()

        if mode == "draw":
            pygame.draw.circle(canvas, color, pos, radius)

        if mode == "eraser":
            pygame.draw.circle(canvas, WHITE, pos, radius)

    # Draw canvas
    screen.blit(canvas, (0,0))

    # ===== MENU / INSTRUCTION =====
    menu_lines = [
        f"Mode: {mode}",
        "D - draw",
        "R - rectangle",
        "C - circle",
        "E - eraser",
        "1-4 - colors",
    ]

    y = 10
    for line in menu_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, y))
        y += 20

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()