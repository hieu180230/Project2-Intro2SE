import pygame as pg
PATH = "data/"

def valid_check(pos: list) -> bool:
    return pos[0] >= 0 and pos[0] <= 9 and pos[1] >= 0 and pos[1] <= 9

def load_img(path):
    img = pg.image.load(f"{PATH}images/{path}").convert_alpha()
    return img

def pos_to_index(pos, cell_size):
    return [p * cell_size for p in pos]