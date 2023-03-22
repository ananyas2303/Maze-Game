import pygame
from value import *
from maze import *
from random import *

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


class Player:
    def __init__(self):
        self.speed = 5
        self.img = pygame.image.load('images/server.png').convert_alpha()
        self.img = pygame.transform.scale(
            self.img, (45, 45))
        self.rect = self.img.get_rect()
        self.rect.center = tile // 2, tile // 2
        self.directions = {'a': (-self.speed, 0), 'd': (self.speed, 0),
                           'w': (0, -self.speed), 's': (0, self.speed)}

    def move(self, direction):
        x, y = self.directions[direction]
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            self.rect = tmp_rect

    def draw(self):
        screen.blit(self.img, self.rect)


player = Player()
op = other_players()
other_players_list = [other_players() for i in range(2)]


def kill_player():
    for other_players in other_players_list:
        if player.rect.collidepoint(other_players.rect.center):
            other_players.set_pos()
            return True
    return False
