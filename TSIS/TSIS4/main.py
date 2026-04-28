import pygame, sys, random, json
from game import *
from db import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# настройки
with open("settings.json") as f:
    settings = json.load(f)

snake_color = tuple(settings["snake_color"])

# БД
init_db()

def input_name():
    name = ""
    while True:
        screen.fill((0,0,0))
        txt = font.render("Enter name:", True, (255,255,255))
        nm = font.render(name, True, (0,255,0))
        screen.blit(txt,(250,250))
        screen.blit(nm,(250,300))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return name if name else "player"
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode


def leaderboard():
    data = get_top_scores()
    while True:
        screen.fill((0,0,0))
        y = 100
        for i,row in enumerate(data):
            t = font.render(f"{i+1}. {row[0]} {row[1]}", True, (255,255,255))
            screen.blit(t,(200,y))
            y+=40

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return


username = input_name()
best = get_best(username)

snake = [(WIDTH//2, HEIGHT//2)]
dx,dy = CELL,0

food = Food(); food.spawn(snake)
poison = Poison(); poison.spawn(snake)
power = None

score = 0
level = 1
delay = 170
last = pygame.time.get_ticks()

obstacles = []

while True:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and dy==0: dx,dy=0,-CELL
            if e.key == pygame.K_DOWN and dy==0: dx,dy=0,CELL
            if e.key == pygame.K_LEFT and dx==0: dx,dy=-CELL,0
            if e.key == pygame.K_RIGHT and dx==0: dx,dy=CELL,0

    now = pygame.time.get_ticks()

    if now-last>delay:
        last=now

        head = ((snake[0][0]+dx)%WIDTH,(snake[0][1]+dy)%HEIGHT)

        if head in snake or head in obstacles:
            break

        snake.insert(0,head)

        if head==food.pos:
            score+=food.value
            food.spawn(snake)

            if score%5==0:
                level+=1
                delay=max(80,delay-10)

                if level>=3:
                    for _ in range(4):
                        obstacles.append(free_cell(snake))

        elif head==poison.pos:
            snake=snake[:-2]
            poison.spawn(snake)
            if len(snake)<=1:
                break

        else:
            snake.pop()

    screen.fill((0,0,0))

    for s in snake:
        pygame.draw.rect(screen,snake_color,(*s,CELL,CELL))

    for o in obstacles:
        pygame.draw.rect(screen,(100,100,100),(*o,CELL,CELL))

    food.draw(screen)
    poison.draw(screen)

    t = font.render(f"{score} lvl:{level} best:{best}", True,(255,255,255))
    screen.blit(t,(10,10))

    pygame.display.update()

save_score(username,score,level)
pygame.quit()