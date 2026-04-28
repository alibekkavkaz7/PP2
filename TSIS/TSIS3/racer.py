import pygame, random

# ---------- ПОЛОСЫ (под большое окно) ----------
LANES = [200, 400, 600]

# ---------- ИГРОК ----------
class Player:
    def __init__(self, img):
        self.image = img
        self.lane = 1
        self.rect = self.image.get_rect(center=(LANES[self.lane], 700))
        self.target_x = LANES[self.lane]
        self.speed = 14
        self.shield = False

    def move(self, direction):
        if direction == "left" and self.lane > 0:
            self.lane -= 1
        if direction == "right" and self.lane < 2:
            self.lane += 1
        self.target_x = LANES[self.lane]

    # плавное движение
    def update(self):
        if self.rect.centerx < self.target_x:
            self.rect.centerx += self.speed
        elif self.rect.centerx > self.target_x:
            self.rect.centerx -= self.speed


# ---------- ВРАГ ----------
class Enemy:
    def __init__(self, img, speed):
        self.image = img
        self.lane = random.randint(0,2)
        self.rect = self.image.get_rect(center=(LANES[self.lane], -150))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


# ---------- МАСЛО ----------
class Oil:
    def __init__(self, speed):
        self.lane = random.randint(0,2)
        self.rect = pygame.Rect(LANES[self.lane]-40, -80, 80, 80)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


# ---------- POWER-UP ----------
class PowerUp:
    def __init__(self, speed):
        self.type = random.choice(["nitro","shield","repair"])
        self.lane = random.randint(0,2)
        self.rect = pygame.Rect(LANES[self.lane]-25, -60, 50, 50)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed