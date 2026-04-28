import pygame, random

LANES = [120, 250, 380]

class Player:
    def __init__(self, img):
        self.lane = 1
        self.y = 550
        self.image = img
        self.rect = self.image.get_rect(center=(LANES[self.lane], self.y))
        self.shield = False

    def move(self, direction):
        if direction == "left" and self.lane > 0:
            self.lane -= 1
        if direction == "right" and self.lane < 2:
            self.lane += 1
        self.rect.centerx = LANES[self.lane]

class Enemy:
    def __init__(self, img, speed):
        self.lane = random.randint(0,2)
        self.image = img
        self.rect = self.image.get_rect(center=(LANES[self.lane], -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

class Oil:
    def __init__(self, speed):
        self.lane = random.randint(0,2)
        self.rect = pygame.Rect(LANES[self.lane]-20, -50, 40, 40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

class PowerUp:
    def __init__(self, speed):
        self.type = random.choice(["nitro","shield","repair"])
        self.lane = random.randint(0,2)
        self.rect = pygame.Rect(LANES[self.lane]-15, -40, 30, 30)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed