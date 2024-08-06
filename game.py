import time
from utils import *
import pygame as pg
import sys
from entity import Agent

DIMENSION = [1080, 720]


class Program:
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("Intro@SE")
        self.font = pg.font.SysFont('Ariel', 16)

        self.log = ""
        self.screen = pg.display.set_mode((DIMENSION[0], DIMENSION[1]))
        self.clock = pg.time.Clock()
        self.player = None
        self.map_data = []
        self.matrix_size = 10
        self.cell_size = None

    def load_map(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            self.matrix_size = int(lines[0])
            self.cell_size = DIMENSION[1]//self.matrix_size
            for line in lines[1:]:
                row = []
                for data in line.strip().split('.'):
                    row.append(data)
                self.map_data.append(row)
        #find blah blah
        self.agent_init()

    def find_position(self, value):
        result = []
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if value in str(self.map_data[i][j]):
                    result.append((i, j))
        return result

    def draw_board(self):
        pg.display.get_surface().fill((255, 255, 255))
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                pg.draw.rect(self.screen, (0, 0, 0), [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size], 1, border_radius=2)
    
    def agent_init(self):
        agent_pos = self.find_position('A')
        self.player = Agent(self,'agent', self.find_position('A')[0], (self.cell_size - 8, self.cell_size - 8), "agent.png")

    def move_log(self):
        words = [word.split(' ') for word in self.log.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.screen.get_size()
        x, y = 740, 3
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, (0, 0, 0))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = 740  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = 740  # Reset the x.
            y += word_height  # Start on new row.

    def run(self):
        self.draw_board()
        time.sleep(1)
        while True:
            (new_pos, log) = self.player.move()
            info = self.map_data[new_pos[0]][new_pos[1]]
            self.player.update(new_pos, info)
            self.log += f"{log}\n"
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.draw_board()
            self.player.render(self.screen, self.cell_size)
            self.move_log()
            time.sleep(1)
            pg.display.update()
            self.clock.tick(60)
