import pygame

# простой рендер текста
def draw_text(screen, text, size, x, y, color=(0,0,0)):
    font = pygame.font.Font("assets/font.ttf", size)
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x,y))
    screen.blit(img, rect)

# главное меню
def main_menu(screen):
    while True:
        screen.fill((230,230,230))
        draw_text(screen, "RACER", 60, 250, 150)

        draw_text(screen, "1 - Play", 30, 250, 300)
        draw_text(screen, "2 - Leaderboard", 30, 250, 350)
        draw_text(screen, "3 - Settings", 30, 250, 400)
        draw_text(screen, "Esc - Quit", 30, 250, 450)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                if event.key == pygame.K_2:
                    return "leaderboard"
                if event.key == pygame.K_3:
                    return "settings"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

# экран лидеров
def leaderboard_screen(screen, scores):
    while True:
        screen.fill((255,255,255))
        draw_text(screen, "Leaderboard", 40, 250, 80)

        y = 150
        for i, s in enumerate(scores):
            draw_text(screen, f"{i+1}. {s['name']} - {s['score']}", 24, 250, y)
            y += 35

        draw_text(screen, "Esc - Back", 20, 250, 650)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

# настройки (очень простые)
def settings_screen(screen, settings):
    while True:
        screen.fill((240,240,240))

        draw_text(screen, f"Sound: {settings['sound']}", 30, 250, 250)
        draw_text(screen, f"Difficulty: {settings['difficulty']}", 30, 250, 320)

        draw_text(screen, "S - toggle sound", 20, 250, 400)
        draw_text(screen, "D - change difficulty", 20, 250, 430)
        draw_text(screen, "Esc - Back", 20, 250, 500)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return settings
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                if e.key == pygame.K_d:
                    settings["difficulty"] = "hard" if settings["difficulty"]=="normal" else "normal"
                if e.key == pygame.K_ESCAPE:
                    return settings