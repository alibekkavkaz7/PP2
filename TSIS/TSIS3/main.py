import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS = 0

COIN_TARGET = 10   # после скольких монет ускоряется игра
BOOSTED = False    # чтобы ускорение сработало один раз

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# создаем окно
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# загружаем ресурсы
background = pygame.image.load("AnimatedStreet.jpg").convert()
crash_sound = pygame.mixer.Sound("crash.wav")

PLAYER_IMG = pygame.transform.scale(
    pygame.image.load("Player.png").convert_alpha(), (80,120)
)

ENEMY_IMG = pygame.transform.scale(
    pygame.image.load("Enemy.png").convert_alpha(), (80,120)
)

# игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=(200,520))

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-7,0)
        if self.rect.right < SCREEN_WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(7,0)

# враг (машина)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=(random.randint(50,350),0))

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)

        # если уехал вниз — возвращаем наверх
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(50,350),0)

# монеты с разным весом
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # случайный вес
        self.value = random.choice([1,2,5])

        # делаем разные размеры и цвета
        if self.value == 1:
            size = 30
            color = (255,215,0)
        elif self.value == 2:
            size = 35
            color = (192,192,192)
        else:
            size = 45
            color = (255,140,0)

        # рисуем круг (вместо картинки)
        self.image = pygame.Surface((size,size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2,size//2), size//2)

        self.rect = self.image.get_rect(center=(random.randint(40,360),0))

    def move(self):
        self.rect.move_ip(0,SPEED)

        # удаляем если ушла за экран
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# создаем объекты
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(P1,E1)

# событие увеличения скорости со временем
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED,1500)

# событие спавна монет
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN,3000)

game_over_flag = False

# основной цикл
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # плавно увеличиваем скорость
        if event.type == INC_SPEED and SPEED < 10:
            SPEED += 0.2

        # создаем монеты
        if event.type == SPAWN_COIN and len(coins) < 5:
            c = Coin()
            coins.add(c)
            all_sprites.add(c)

    if not game_over_flag:

        DISPLAYSURF.blit(background,(0,0))

        # вывод счета
        DISPLAYSURF.blit(
            font_small.render(f"Score: {SCORE}",True,BLACK),
            (10,10)
        )

        coin_text = font_small.render(f"Coins: {COINS}",True,BLACK)
        DISPLAYSURF.blit(coin_text, coin_text.get_rect(topright=(390,10)))

        # рисуем и двигаем все объекты
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image,entity.rect)
            entity.move()

        # столкновение с врагом
        if pygame.sprite.spritecollideany(P1,enemies):
            crash_sound.play()
            game_over_flag = True
            game_over_text = font.render("Game Over",True,RED)

        # сбор монет
        collected = pygame.sprite.spritecollide(P1,coins,True)
        if collected:
            for coin in collected:
                COINS += coin.value

        # ускорение при достижении N монет
        if COINS >= COIN_TARGET and not BOOSTED:
            SPEED += 3
            BOOSTED = True

    else:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(game_over_text,(50,250))

    pygame.display.update()
    FramePerSec.tick(FPS)