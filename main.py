from maze import *
import pygame
from network import *
from value import *
from random import randrange

maze = generate_maze()
walls_collide_list = sum([cell.get_rects() for cell in maze], [])


class other_players:
    def __init__(self):
        self.img = pygame.image.load('images/one.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (45, 45))
        self.rect = self.img.get_rect()
        self.set_pos()
        self.speed = 0.1

    def set_pos(self):
        while True:
            self.coor = self.rect.topleft = randrange(
                column) * tile + 5, randrange(row) * tile + 5
            if self.rect.collidelist(walls_collide_list) == -1:
                break

    def draw(self):
        screen.blit(self.img, self.rect)

    def move(self, direction, x, y):
        if direction == 'left':
            x = -self.speed * tile
        elif direction == 'right':
            x = self.speed * tile
        elif direction == 'up':
            y = -self.speed * tile
        elif direction == 'down':
            y = self.speed * tile
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            self.rect = tmp_rect


class Player:
    def __init__(self):
        self.speed = 5
        self.img = pygame.image.load('images/server.png').convert_alpha()
        self.img = pygame.transform.scale(
            self.img, (45, 45))
        self.rect = self.img.get_rect()
        self.rect.center = tile // 2, tile // 2
        # self.directions = {'a': (-self.speed, 0), 'd': (self.speed, 0),'w': (0, -self.speed), 's': (0, self.speed)}

    def move(self, direction):
        x, y = 0, 0
        if direction == 'left':
            x = -self.speed * tile
        elif direction == 'right':
            x = self.speed * tile
        elif direction == 'up':
            y = -self.speed * tile
        elif direction == 'down':
            y = self.speed * tile
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            self.rect = tmp_rect

    def draw(self):
        screen.blit(self.img, self.rect)


def kill_player():
    for other_players in other_players_list:
        if player.rect.collidepoint(other_players.rect.center):
            other_players.set_pos()
            return True
    return False


def is_game_over():
    pass


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


FPS = 60
pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player = Player()
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
other_players_list = [other_players() for i in range(2)]

# get position from the server
n = Network()

while True:
    surface.blit(screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            pygame.quit()
    startpos = read_pos(n.get_pos())
    a = startpos[0]
    b = startpos[1]
    p2pos = read_pos(n.send(make_pos((a, b))))
    c = p2pos[0]
    d = p2pos[1]
    pressedkey = pygame.key.get_pressed()
    if pressedkey[pygame.K_j]:
        other_players_list[0].move('left', a, b)
    elif pressedkey[pygame.K_l]:
        other_players_list[0].move('right', a, b)
    elif pressedkey[pygame.K_i]:
        other_players_list[0].move('up', a, b)
    elif pressedkey[pygame.K_k]:
        other_players_list[0].move('down', a, b)
    if pressedkey[pygame.K_s]:
        other_players_list[1].move('left', c, d)
    elif pressedkey[pygame.K_a]:
        other_players_list[1].move('right', c, d)
    elif pressedkey[pygame.K_d]:
        other_players_list[1].move('up', c, d)
    elif pressedkey[pygame.K_w]:
        other_players_list[1].move('down', c, d)
    if pressedkey[pygame.K_LEFT]:
        player.move('left')
    elif pressedkey[pygame.K_RIGHT]:
        player.move('right')
    elif pressedkey[pygame.K_UP]:
        player.move('up')
    elif pressedkey[pygame.K_DOWN]:
        player.move('down')

    for cell in maze:
        cell.draws(screen)
    if kill_player():
        exit()
    is_game_over()
    player.draw()
    for other_players in other_players_list:
        other_players.draw()
    pygame.display.flip()
    clock.tick(FPS)
