import random
import time
from enum import Enum
from utils import *
import pygame as pg

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
class Compass(Enum):
    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3

class Agent:
    def __init__(self, game, type, pos, size, path):
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.cell_info = None
        self.facing_dir = Compass.NORTH
        self.img = load_img(path)
        self.img = pg.transform.smoothscale(self.img, size)

    def turn_left(self):
        self.img = pg.transform.rotate(self.img, 90)
        return f"Turn left: {self.pos}\n"
    def turn_right(self):
        self.img = pg.transform.rotate(self.img, -90)
        return f"Turn right: {self.pos}\n"
    def forward(self, new_pos):
        return f"Forward: {new_pos}\n"


    def update(self, newpos, info):
        self.pos[0] = newpos[0]
        self.pos[1] = newpos[1]
        self.cell_info = info

    def render(self, surface, cell_size):
        render_pos = self.pos.copy()
        render_pos[0] = render_pos[0] * cell_size + 4
        render_pos[1] = render_pos[1] * cell_size + 4
        surface.blit(self.img, render_pos)

    def get_neighbors(self):
        neighbors = [list(self.pos[0] + d[0], self.pos[1] + d[1]) for d in directions]
        return [n for n in neighbors if self.is_valid(n)]

    def change_direction(self, action):
        if directions[action][0] == 0:
            if directions[action][1] == 1:
                self.facing_dir = Compass.SOUTH
            else:
                self.facing_dir = Compass.NORTH
        elif directions[action][1] == 0:
            if directions[action][0] == 1:
                self.facing_dir = Compass.EAST
            else:
                self.facing_dir = Compass.WEST

    def generate_move(self):
        return random.choice([0, 1, 2, 3])
    def move(self):
        log = f"Current: {self.pos} | Facing {self.facing_dir}\n"

        new_pos = self.pos
        while True:
            action = self.generate_move()
            uncheck_pos = new_pos
            uncheck_pos[0] += directions[action][0]
            uncheck_pos[1] += directions[action][1]
            if valid_check(uncheck_pos):
                new_pos = uncheck_pos
                break
        #print(f"  Action: {action} ")
        if self.facing_dir.value == action:
            log += self.forward(new_pos)
        elif abs(self.facing_dir.value - action) == 2:
            log += self.turn_left()
            log += self.turn_left()
            log += self.forward(new_pos)
            self.change_direction(action)
        elif self.facing_dir.value - action == -1 or self.facing_dir.value - action == 3:
            log += self.turn_left()
            log += self.forward(new_pos)
            self.change_direction(action)
        elif self.facing_dir.value - action == 1 or self.facing_dir.value - action == -3:
            log += self.turn_right()
            log += self.forward(new_pos)
            self.change_direction(action)
        log += f"Current: {self.pos} Facing {self.facing_dir}\n-----move done-------\n"
        return (new_pos, log)
