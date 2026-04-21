# Imports
import pygame, sys
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS = 0

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Assets
background = pygame.image.load("AnimatedStreet.jpg")
crash_sound = pygame.mixer.Sound("crash.wav")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (80,120))
        self.rect = self.image.get_rect(center=(200,520))

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-7,0)
        if self.rect.right < SCREEN_WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(7,0)

# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (80,120))
        self.rect = self.image.get_rect(center=(random.randint(50,350),0))

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(50,350),0)

# ================= COIN =================
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (45,45))
        self.rect = self.image.get_rect(center=(random.randint(40,360),0))

    def move(self):
        self.rect.move_ip(0,SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# INIT
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(P1, E1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1500)

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 3500)

game_over_flag = False

# LOOP
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED and SPEED < 10:
            SPEED += 0.3

        if event.type == SPAWN_COIN and len(coins) < 4:
            c = Coin()
            coins.add(c)
            all_sprites.add(c)

    if not game_over_flag:

        DISPLAYSURF.blit(background, (0,0))

        # text
        DISPLAYSURF.blit(font_small.render(f"Score: {SCORE}", True, BLACK),(10,10))

        coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
        DISPLAYSURF.blit(coin_text, coin_text.get_rect(topright=(390,10)))

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # enemy collision
        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play()
            game_over_flag = True
            game_over_text = font.render("Game Over", True, RED)

        # coin collision
        collected = pygame.sprite.spritecollide(P1, coins, True)
        if collected:
            COINS += len(collected)

    else:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(game_over_text, (50,250))

    pygame.display.update()
    FramePerSec.tick(FPS)