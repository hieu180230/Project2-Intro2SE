import pygame as pg
PATH = "data/"

def valid_check(pos: list) -> bool:
    return pos[0] >= 0 and pos[0] <= 9 and pos[1] >= 0 and pos[1] <= 9

def get_neighbors(position):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = [(position[0] + d[0], position[1] + d[1]) for d in directions]
    return [n for n in neighbors if valid_check(n)]

def load_img(path):
    img = pg.image.load(f"{PATH}images/{path}").convert_alpha()
    return img

def pos_to_index(pos, cell_size):
    return [p * cell_size for p in pos]