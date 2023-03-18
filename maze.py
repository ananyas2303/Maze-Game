import pygame
from random import choice
from value import *


class cell:
    def __init__(self, x, y):
        super().__init__()
        # self.game = game
        # self.group = self.game.all_sprites, self.game.walls
        # pygame.sprite.Sprite.__init__(self, self.group)
        self.x = x
        self.y = y
        self.thickness = 4
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draws(self, screen):
        x = self.x*tile
        y = self.y*tile
        # img = pygame.image.load('wall.png')
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, tile, tile))
        if self.walls['top']:
            pygame.draw.line(screen, YELLOW, (x, y), (x+tile, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, YELLOW, (x+tile, y), (x+tile, y+tile), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, YELLOW, (x+tile, y+tile), (x, y+tile), 2)
        if self.walls['left']:
            pygame.draw.line(screen, YELLOW, (x, y+tile), (x, y), 2)

    def get_rects(self):
        rects = []
        x, y = self.x * tile, self.y * tile
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (tile, 2)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + tile, y), (2, tile)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + tile), (tile, 2)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (2, tile)))
        return rects

    def check_cell(self, x, y):
        # def find_index(x, y): return x+y*column
        def find_index(x, y): return x + y * column
        if x < 0 or x > column-1 or y < 0 or y > row-1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbour(self, grid_cells):
        neighbour = []
        top = self.check_cell(self.x, self.y-1)
        right = self.check_cell(self.x+1, self.y)
        bottom = self.check_cell(self.x, self.y+1)
        left = self.check_cell(self.x-1, self.y)
        if top and not top.visited:
            neighbour.append(top)
        if right and not right.visited:
            neighbour.append(right)
        if bottom and not bottom.visited:
            neighbour.append(bottom)
        if left and not left.visited:
            neighbour.append(left)

        if neighbour:
            return choice(neighbour)
        else:
            False


def eliminate_wall(current, next):
    wall_x = current.x-next.x
    if wall_x == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif wall_x == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    wall_y = current.y-next.y
    if wall_y == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif wall_y == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


grid_cells = [cell(col, rows) for rows in range(row)
              for col in range(column)]


def generate_maze():

    current = grid_cells[0]
    stack = []
    count = 1
    while count != len(grid_cells):
        current.visited = True
        # current.draw_curr(screen)
        next_cell = current.check_neighbour(grid_cells)
        if next_cell:
            next_cell.visited = True
            count += 1
            stack.append(current)
            eliminate_wall(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
    return grid_cells
