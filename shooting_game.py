import pygame
from pygame.locals import *
import math
from random import randint

# Hi girls

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption('ShootV2')
score = 0
score_text = 'Score:'
score_x, score_y, fontSize = 15, 550, 50
myFont = pygame.font.SysFont('None', fontSize)
fontColor = (0, 255, 0)
max_enemies = 2
enemies_speed_boost = 1.0
death_font = pygame.font.SysFont('None', 100)
death_text = 'YOU DIED'
death_color = (255, 0, 0)
pause_text = 'PAUSE'


def circle_col_check(x1, y1, rad1, x2, y2, rad2):
    collision = False
    if x1 + rad1 >= x2 - rad2 and x1 <= x2:  # СЛЕВА
        if y1 - rad1 <= y2 + rad2 and y1 >= y2:  # СНИЗУ
            collision = True
        elif y1 + rad1 >= y2 - rad2 and y2 >= y1:  # СВЕРХУ
            collision = True
    elif x1 - rad1 <= x2 + rad2 and x1 >= x2:  # СПРАВА
        if y1 - rad1 <= y2 + rad2 and y1 >= y2:  # СНИЗУ
            collision = True
        elif y1 + rad1 >= y2 - rad2 and y2 >= y1:  # СВЕРХУ
            collision = True
    return collision


def bullet_speed(st_x, st_y, fin_x, fin_y):
    angle = math.atan2((fin_y - st_y), (fin_x - st_x))
    x_speed_k = math.cos(angle)
    y_speed_k = math.sin(angle)
    return x_speed_k, y_speed_k


class Player:
    pos = (300, 300)
    rad = 10
    color = (0, 255, 0)

    def draw_player(self):
        pygame.draw.circle(win, self.color, self.pos, self.rad)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.st_x = x
        self.st_y = y
        self.rad = 15
        self.color = (255, 0, 255)
        self.vel = 1
        self.fin_x = player.pos[0]
        self.fin_y = player.pos[1]
        speed_ks = bullet_speed(self.st_x, self.st_y, self.fin_x, self.fin_y)
        self.x_speed = self.vel * speed_ks[0]
        self.y_speed = self.vel * speed_ks[1]

    def draw_enemy_and_move(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.rad)
        self.x += self.x_speed * enemies_speed_boost
        self.y += self.y_speed * enemies_speed_boost


class Shot:
    def __init__(self, fin_x, fin_y):
        self.x = player.pos[0]
        self.y = player.pos[1]
        self.st_y = player.pos[1]
        self.st_x = player.pos[0]
        self.fin_x = fin_x
        self.fin_y = fin_y
        self.rad = 5
        self.vel = 10
        self.color = (0, 0, 255)
        speed_ks = bullet_speed(self.st_x, self.st_y, self.fin_x, self.fin_y)
        self.x_speed = self.vel * speed_ks[0]
        self.y_speed = self.vel * speed_ks[1]

    def draw_shot_and_move(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.rad)
        self.x += self.x_speed
        self.y += self.y_speed


player = Player()
shots = []
enemies = []


def random_enemy():
    wall = randint(1, 4)
    x = 0
    y = 0
    if wall == 1:
        x = 0
        y = randint(0, 600)
    elif wall == 2:
        y = 0
        x = randint(0, 600)
    elif wall == 3:
        x = 600
        y = randint(0, 600)
    elif wall == 4:
        y = 600
        x = randint(1, 6)
    return x, y


def draw_game():
    global score
    global working
    win.fill((0, 0, 0))
    player.draw_player()
    for shot in shots:
        shot.draw_shot_and_move()
        shot_deleted = False
        for enemy in enemies:
            if circle_col_check(shot.x, shot.y, shot.rad, enemy.x, enemy.y, enemy.rad):
                enemies.pop(enemies.index(enemy))
                shots.pop(shots.index(shot))
                score += 10
                shot_deleted = True
        if (shot.x > 600 or shot.y > 600 or shot.x < 0 or shot.y < 0) and not shot_deleted:
            shots.pop(shots.index(shot))
    for enemy in enemies:
        enemy.draw_enemy_and_move()
        if circle_col_check(player.pos[0], player.pos[1], player.rad, enemy.x, enemy.y, enemy.rad):
            death_image = death_font.render(death_text, 5, death_color)
            win.blit(death_image, (140, 200))
            font_image = myFont.render(score_text + str(score), 5, fontColor)
            win.blit(font_image, (140, 300))
            pygame.display.update()
            pygame.time.delay(5000)
            print('Game over')
            working = False
    font_image = myFont.render(score_text + str(score), 5, fontColor)
    win.blit(font_image, (score_x, score_y))
    pygame.display.update()


pause = False
working = True
while working:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                working = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                shots.append(Shot(event.pos[0], event.pos[1]))
            if event.button == 3:
                pause = True
    while pause:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                working = False
                pause = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    working = False
                    pause = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    pause = False
        pauseImage = death_font.render(pause_text, 10, (255, 255, 255))
        win.blit(pauseImage, (190, 200))
        pygame.display.update()

    if len(enemies) < max_enemies:
        enemy_pos = random_enemy()
        enemies.append(Enemy(enemy_pos[0], enemy_pos[1]))
        enemies_speed_boost += 0.05
    draw_game()
pygame.quit()
