import pygame
import random
import math

SCREEN_WIDTH = 1200
ROAD_LEFT = 100
ROAD_RIGHT = SCREEN_WIDTH - 100


# Игрок
class Player:
    def __init__(self, img):
        self.image = img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 740))

        # Хитбокс делаем меньше картинки, чтобы не было ложных столкновений
        self.hitbox = self.rect.inflate(-110, -130)

        self.vel_x = 0.0
        self.base_acc = 1.0
        self.base_max_speed = 10.0
        self.acc = self.base_acc
        self.max_speed = self.base_max_speed
        self.friction = 0.85

        # Щит: один удар можно пережить
        self.shield_hits = 0

        # Эффект масла
        self.wobble_until = 0
        self.wobble_phase = 0.0
        self.wobble_strength = 0

    def set_nitro(self, active):
        # Нитро усиливает ускорение и максимальную скорость
        if active:
            self.acc = self.base_acc * 1.6
            self.max_speed = self.base_max_speed + 6
        else:
            self.acc = self.base_acc
            self.max_speed = self.base_max_speed

    def start_wobble(self, duration_ms):
        # После масла машина начинает вилять несколько секунд
        now = pygame.time.get_ticks()
        self.wobble_until = now + duration_ms
        self.wobble_strength = random.randint(8, 14)
        self.wobble_phase = 0.0

    def update(self):
        keys = pygame.key.get_pressed()

        # Управление влево и вправо
        if keys[pygame.K_LEFT]:
            self.vel_x -= self.acc
        if keys[pygame.K_RIGHT]:
            self.vel_x += self.acc

        # Ограничиваем скорость движения
        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))

        # Трение, чтобы машина не скользила бесконечно
        self.vel_x *= self.friction

        now = pygame.time.get_ticks()

        # Если действует масло, добавляем боковое виляние
        wobble_offset = 0
        if now < self.wobble_until:
            self.wobble_phase += 0.35
            wobble_offset = int(math.sin(self.wobble_phase) * self.wobble_strength)

        self.rect.x += int(self.vel_x) + wobble_offset

        # Границы дороги
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
            self.vel_x = 0
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT
            self.vel_x = 0

        # Хитбокс двигается вместе с машиной
        self.hitbox.center = self.rect.center


# Вражеская машина
class Enemy:
    def __init__(self, img, speed, x):
        self.image = img
        self.rect = self.image.get_rect(center=(x, -220))
        self.hitbox = self.rect.inflate(-110, -130)
        self.speed = speed

    def update(self, speed_bonus=0):
        self.rect.y += int(self.speed + speed_bonus)
        self.hitbox.center = self.rect.center


# Масло
class Oil:
    def __init__(self, img, speed, x):
        self.image = img
        self.rect = self.image.get_rect(center=(x, -120))
        self.speed = speed

    def update(self, speed_bonus=0):
        self.rect.y += int(self.speed + speed_bonus)


# Power-up
class PowerUp:
    def __init__(self, images, speed, x):
        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = images[self.type]
        self.rect = self.image.get_rect(center=(x, -120))
        self.speed = speed

    def update(self, speed_bonus=0):
        self.rect.y += int(self.speed + speed_bonus)


# Монета
class Coin:
    def __init__(self, speed, x):
        self.value = random.choice([1, 2, 5])

        # Чем больше value, тем монета крупнее
        if self.value == 1:
            size = 40
            color = (255, 215, 0)
        elif self.value == 2:
            size = 50
            color = (192, 192, 192)
        else:
            size = 60
            color = (255, 140, 0)

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)

        self.rect = self.image.get_rect(center=(x, -100))
        self.speed = speed

    def update(self, speed_bonus=0):
        self.rect.y += int(self.speed + speed_bonus)