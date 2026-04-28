import pygame
import random

WIDTH, HEIGHT = 700, 700
CELL = 20

def free_cell(snake, blocked=None):
    blocked = set(blocked or [])
    while True:
        pos = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )
        if pos not in snake and pos not in blocked:
            return pos


class Food:
    def spawn(self, snake, blocked=None):
        self.pos = free_cell(snake, blocked)
        self.value = random.choice([1,2,3])
        self.time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), (*self.pos, CELL, CELL))


class Poison:
    def spawn(self, snake, blocked=None):
        self.pos = free_cell(snake, blocked)

    def draw(self, screen):
        pygame.draw.rect(screen, (120,0,120), (*self.pos, CELL, CELL))


class PowerUp:
    def spawn(self, snake, blocked=None):
        self.type = random.choice(["speed","slow","shield"])
        self.pos = free_cell(snake, blocked)
        self.time = pygame.time.get_ticks()

    def draw(self, screen):
        colors = {
            "speed": (0,200,255),
            "slow": (255,255,0),
            "shield": (0,255,0)
        }
        pygame.draw.rect(screen, colors[self.type], (*self.pos, CELL, CELL))