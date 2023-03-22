from maze import *
import pygame
from network import *
from value import *
from sprites import *

maze = generate_maze()
walls_collide_list = sum([cell.get_rects() for cell in maze], [])


def is_game_over():
    pass


FPS = 60
pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# get position from the server
n = Network()

while True:
    surface.blit(screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            pygame.quit()
    pressedkey = pygame.key.get_pressed()
    if pressedkey[pygame.K_j]:
        other_players_list[0].move('left')
    elif pressedkey[pygame.K_l]:
        other_players_list[0].move('right')
    elif pressedkey[pygame.K_i]:
        other_players_list[0].move('up')
    elif pressedkey[pygame.K_k]:
        other_players_list[0].move('down')
    if pressedkey[pygame.K_f]:
        other_players_list[1].move('left')
    elif pressedkey[pygame.K_h]:
        other_players_list[1].move('right')
    elif pressedkey[pygame.K_t]:
        other_players_list[1].move('up')
    elif pressedkey[pygame.K_g]:
        other_players_list[1].move('down')
    if pressedkey[pygame.K_LEFT]:
        player.move('a')
    elif pressedkey[pygame.K_RIGHT]:
        player.move('d')
    elif pressedkey[pygame.K_UP]:
        player.move('w')
    elif pressedkey[pygame.K_DOWN]:
        player.move('s')

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
