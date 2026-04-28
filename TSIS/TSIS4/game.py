import pygame
import random

WIDTH, HEIGHT = 400, 400
CELL = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
PURPLE = (150,0,150)  # яд


# обычная еда
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.pos = (random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL))
        self.value = random.choice([1,2,3])
        self.time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.pos, CELL, CELL))


# ядовитая еда
class Poison:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.pos = (random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL))

    def draw(self, screen):
        pygame.draw.rect(screen, PURPLE, (*self.pos, CELL, CELL))


# power-up
class PowerUp:
    def __init__(self):
        self.type = random.choice(["speed","slow","shield"])
        self.spawn_time = pygame.time.get_ticks()
        self.pos = (random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL))

    def draw(self, screen):
        color = {
            "speed": (0,255,255),
            "slow": (255,255,0),
            "shield": (0,255,0)
        }
        pygame.draw.rect(screen, color[self.type], (*self.pos, CELL, CELL))