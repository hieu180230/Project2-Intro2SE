import time
from utils import *
import pygame as pg
import sys
from entity import Agent
from pygame.locals import *
from pygame.locals import *
import gc


DIMENSION = [1080, 720]
DATA_TO_NAME = {
    "S": "stench",
    "W_H": "whiff",
    "B": "breeze",
    "G_L": "glow"
}

class Program:
    def __init__(self):
        flags = DOUBLEBUF

        #pg.init()
        pg.font.init()
        pg.display.init()
        pg.mixer.init()
        pg.display.set_caption("Intro@SE")
        self.font = pg.font.SysFont('Ariel', 16)

        self.log = ""
        self.screen = pg.display.set_mode((DIMENSION[0], DIMENSION[1]), flags, 16)
        self.clock = pg.time.Clock()
        self.player = None
        self.map_data = []
        self.matrix_size = 10
        self.cell_size = None
        self.element_position = {}

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
        for x in self.map_data:
            print(x)
        self.element_position["wumpus"] = self.find_position("W")
        for position in self.element_position["wumpus"]:
            for neighbor in get_neighbors(position):
                if self.map_data[neighbor[0]][neighbor[1]] == '-':
                    self.map_data[neighbor[0]][neighbor[1]] = 'S'
                else:
                    self.map_data[neighbor[0]][neighbor[1]] += ',S'
        self.element_position["pit"] = self.find_position("P")
        for position in self.element_position["pit"]:
            for neighbor in get_neighbors(position):
                if self.map_data[neighbor[0]][neighbor[1]] == '-':
                    self.map_data[neighbor[0]][neighbor[1]] = 'B'
                else:
                    self.map_data[neighbor[0]][neighbor[1]] += ',B'
        self.element_position["gold"] = self.find_position("G")
        self.element_position["poisonous_gas"] = self.find_position("P_G")
        for position in self.element_position["poisonous_gas"]:
            for neighbor in get_neighbors(position):
                if self.map_data[neighbor[0]][neighbor[1]] == '-':
                    self.map_data[neighbor[0]][neighbor[1]] = 'W_H'
                else:
                    self.map_data[neighbor[0]][neighbor[1]] += ',W_H'
        self.element_position["healing_potion"] = self.find_position("H_P")
        for position in self.element_position["healing_potion"]:
            for neighbor in get_neighbors(position):
                if self.map_data[neighbor[0]][neighbor[1]] == '-':
                    self.map_data[neighbor[0]][neighbor[1]] = 'G_L'
                else:
                    self.map_data[neighbor[0]][neighbor[1]] += ',G_L'

        #find blah blah
        self.agent_init()

    def map_state_output(self):
        map_state = ""
        for element in self.element_position:
            map_state += f"{element.replace('_', ' ')}: {len(self.element_position[element])}\n"

        words = [word.split(' ') for word in map_state.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.screen.get_size()
        x, y = 740, 600
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

    def find_position(self, value):
        result = []
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if value == str(self.map_data[i][j]).split(',')[0]:
                    result.append((i, j))
        return result

    def render_elements(self):
        size = (self.cell_size - 8, self.cell_size - 8)
        for element_pos in self.element_position:
            img = load_img(f"{element_pos}.png")
            for pos in self.element_position[element_pos]:
                self.render_element(img, pos, size)
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                if self.map_data[x][y] == '-':
                    continue
                if size[0] == self.cell_size - 8:
                    size = [(s / 2) for s in size]
                if 'S' in self.map_data[x][y]:
                    img = load_img(f"{DATA_TO_NAME['S']}.png")
                    self.render_element(img, (x, y), size)
                if 'B' in self.map_data[x][y]:
                    img = load_img(f"{DATA_TO_NAME['B']}.png")
                    self.render_element(img, (x + 0.5, y), size)
                if 'W' in self.map_data[x][y]:
                    img = load_img(f"{DATA_TO_NAME['W_H']}.png")
                    self.render_element(img, (x, y + 0.5), size)
                if 'G_L' in self.map_data[x][y]:
                    img = load_img(f"{DATA_TO_NAME['G_L']}.png")
                    self.render_element(img, (x + 0.5, y + 0.5), size)

    def render_element(self, img, pos, size):
        img = pg.transform.scale(img, size)
        render_pos = list(pos).copy()
        render_pos[0] = render_pos[0] * self.cell_size + 4
        render_pos[1] = render_pos[1] * self.cell_size + 4
        render_pos.reverse()
        self.screen.blit(img, render_pos)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                pg.draw.rect(self.screen, (0, 0, 0), [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size], 1, border_radius=2)
        self.render_elements()
    def agent_init(self):
        agent_pos = self.find_position('A')
        self.player = Agent(self, self.find_position('A')[0], (self.cell_size - 8, self.cell_size - 8), "agent.png")

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
            if y >= 500:
                new_rect = pg.rect.Rect(DIMENSION[0] - 340, 0, 340, DIMENSION[1])
                pg.draw.rect(self.screen, (255, 255, 255), new_rect)
                y = 3

    def run(self):
        self.draw_board()
        while True:
            gc.collect()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    print("ready")
                    (new_pos, log) = self.player.move()
                    info = self.map_data[new_pos[0]][new_pos[1]]
                    self.player.update(new_pos, info)
                    self.log += f"{log}\n"
                    self.draw_board()
                    self.move_log()
                    self.map_state_output()
                    self.player.render(self.screen, self.cell_size)
            pg.display.update()
            self.clock.tick(60)

