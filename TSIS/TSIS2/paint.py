import pygame
import sys
from datetime import datetime
from tools import flood_fill

pygame.init()

# ---------- ОКНО ----------
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# ---------- ЦВЕТА ----------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

color = BLACK

# ---------- ТОЛЩИНА ----------
sizes = {1:2, 2:5, 3:10}
brush = sizes[2]

# ---------- РЕЖИМ ----------
mode = "draw"
start_pos = None
drawing = False
last_pos = None

# ---------- ТЕКСТ ----------
typing = False
text = ""
text_pos = None

# используем шрифт из assets
font = pygame.font.Font("assets/font.ttf", 20)

# ---------- ХОЛСТ ----------
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------- КЛАВИАТУРА ----------
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d: mode = "draw"
            if event.key == pygame.K_l: mode = "line"
            if event.key == pygame.K_r: mode = "rect"
            if event.key == pygame.K_c: mode = "circle"
            if event.key == pygame.K_e: mode = "eraser"
            if event.key == pygame.K_f: mode = "fill"
            if event.key == pygame.K_t: mode = "text"
            if event.key == pygame.K_s: mode = "square"
            if event.key == pygame.K_g: mode = "triangle"
            if event.key == pygame.K_q: mode = "equilateral"
            if event.key == pygame.K_h: mode = "rhombus"

            if event.key == pygame.K_1: color = RED
            if event.key == pygame.K_2: color = GREEN
            if event.key == pygame.K_3: color = BLUE
            if event.key == pygame.K_4: color = BLACK

            if event.key == pygame.K_z: brush = sizes[1]
            if event.key == pygame.K_x: brush = sizes[2]
            if event.key == pygame.K_v: brush = sizes[3]

            # сохранение
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name = datetime.now().strftime("paint_%H%M%S.png")
                pygame.image.save(canvas, name)

            # ввод текста
            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text, True, color)
                    canvas.blit(img, text_pos)
                    typing = False
                    text = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text = ""
                else:
                    text += event.unicode

        # ---------- МЫШЬ ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            drawing = True
            last_pos = event.pos

            if mode == "fill":
                flood_fill(canvas, start_pos[0], start_pos[1], color)

            if mode == "text":
                typing = True
                text = ""
                text_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "line":
                pygame.draw.line(canvas, color, start_pos, end_pos, brush)

            if mode == "rect":
                rect = pygame.Rect(start_pos[0], start_pos[1],
                                   end_pos[0]-start_pos[0],
                                   end_pos[1]-start_pos[1])
                pygame.draw.rect(canvas, color, rect, brush)

            if mode == "circle":
                r = int(((end_pos[0]-start_pos[0])**2 +
                         (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, r, brush)

            if mode == "square":
                size = max(abs(end_pos[0]-start_pos[0]),
                           abs(end_pos[1]-start_pos[1]))
                rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                pygame.draw.rect(canvas, color, rect, brush)

            if mode == "triangle":
                points = [start_pos, (end_pos[0], start_pos[1]), end_pos]
                pygame.draw.polygon(canvas, color, points, brush)

            if mode == "equilateral":
                x1,y1 = start_pos
                x2,y2 = end_pos
                w = x2 - x1
                h = abs(w) * 0.866
                points = [(x1,y1),(x2,y1),(x1+w//2, y1-h)]
                pygame.draw.polygon(canvas, color, points, brush)

            if mode == "rhombus":
                x1,y1 = start_pos
                x2,y2 = end_pos
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                points = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
                pygame.draw.polygon(canvas, color, points, brush)

    # ---------- РИСОВАНИЕ ----------
    if drawing:
        pos = pygame.mouse.get_pos()

        if mode == "draw":
            pygame.draw.line(canvas, color, last_pos, pos, brush)
            last_pos = pos

        if mode == "eraser":
            pygame.draw.line(canvas, WHITE, last_pos, pos, brush)
            last_pos = pos

    # ---------- ОТРИСОВКА ----------
    screen.blit(canvas, (0,0))

    if mode == "line" and drawing:
        pygame.draw.line(screen, color, start_pos, pygame.mouse.get_pos(), 1)

    if typing:
        img = font.render(text, True, color)
        screen.blit(img, text_pos)

    # меню
    menu = [
        f"Mode: {mode}",
        "D draw | L line | R rect | C circle",
        "S square | G triangle | Q equilateral | H rhombus",
        "F fill | T text | E eraser",
        "Z/X/V size | 1-4 colors",
        "Ctrl+S save"
    ]

    y = 10
    for line in menu:
        screen.blit(font.render(line, True, BLACK), (10,y))
        y += 20

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()