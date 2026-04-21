import pygame
import sys

pygame.init()

# ---------- ОКНО ----------
WIDTH, HEIGHT = 800, 600
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
radius = 5

# ---------- РЕЖИМЫ ----------
mode = "draw"
start_pos = None

# ---------- ХОЛСТ ----------
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# ---------- ШРИФТ ----------
font = pygame.font.SysFont("Arial", 18)

running = True
while running:

    # ---------- СОБЫТИЯ ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- клавиатура ---
        if event.type == pygame.KEYDOWN:

            # режимы рисования
            if event.key == pygame.K_d: mode = "draw"
            if event.key == pygame.K_r: mode = "rect"
            if event.key == pygame.K_c: mode = "circle"
            if event.key == pygame.K_e: mode = "eraser"

            # дополнительные фигуры
            if event.key == pygame.K_s: mode = "square"
            if event.key == pygame.K_t: mode = "triangle"
            if event.key == pygame.K_q: mode = "equilateral"
            if event.key == pygame.K_h: mode = "rhombus"

            # выбор цвета
            if event.key == pygame.K_1: color = RED
            if event.key == pygame.K_2: color = GREEN
            if event.key == pygame.K_3: color = BLUE
            if event.key == pygame.K_4: color = BLACK

        # --- нажали мышь ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

        # --- отпустили мышь (рисуем фигуры) ---
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos

            # прямоугольник
            if mode == "rect":
                rect = pygame.Rect(start_pos[0], start_pos[1],
                                   end_pos[0]-start_pos[0],
                                   end_pos[1]-start_pos[1])
                pygame.draw.rect(canvas, color, rect, 2)

            # круг
            if mode == "circle":
                r = int(((end_pos[0]-start_pos[0])**2 +
                         (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, r, 2)

            # квадрат
            if mode == "square":
                size = max(abs(end_pos[0]-start_pos[0]),
                           abs(end_pos[1]-start_pos[1]))
                rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                pygame.draw.rect(canvas, color, rect, 2)

            # прямоугольный треугольник
            if mode == "triangle":
                points = [
                    start_pos,
                    (end_pos[0], start_pos[1]),
                    end_pos
                ]
                pygame.draw.polygon(canvas, color, points, 2)

            # равносторонний треугольник
            if mode == "equilateral":
                x1,y1 = start_pos
                x2,y2 = end_pos
                w = x2 - x1
                h = abs(w) * 0.866
                points = [
                    (x1,y1),
                    (x2,y1),
                    (x1 + w//2, y1 - h)
                ]
                pygame.draw.polygon(canvas, color, points, 2)

            # ромб
            if mode == "rhombus":
                x1,y1 = start_pos
                x2,y2 = end_pos
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                points = [
                    (cx,y1),
                    (x2,cy),
                    (cx,y2),
                    (x1,cy)
                ]
                pygame.draw.polygon(canvas, color, points, 2)

    # ---------- РИСОВАНИЕ / ЛАСТИК ----------
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()

        if mode == "draw":
            pygame.draw.circle(canvas, color, pos, radius)

        if mode == "eraser":
            pygame.draw.circle(canvas, WHITE, pos, radius)

    # ---------- ОТРИСОВКА ----------
    screen.blit(canvas, (0,0))

    # ---------- МЕНЮ ----------
    menu = [
        f"Mode: {mode}",
        "D - draw | R - rect | C - circle",
        "S - square | T - triangle",
        "Q - equilateral | H - rhombus",
        "E - eraser",
        "1-4 - colors"
    ]

    y = 10
    for line in menu:
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, y))
        y += 20

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()