import pygame
import random
import time
from pygame import *


class Cell:
    def set_state(self, state):
        self.state = state


    def is_alive(self):
        return self.state


class CellList:
    def __init__(self, nrow = 10, ncol = 10, filename = None):
        self.nrow = nrow
        self.ncol = ncol
        self.filename = filename
        
        grid = [[Cell(0) for i in range(ncol)] for j in range(nrow)]
        if filename != None:
            fin = open(filename)
            for i in range(nrow):
                grid[i] = [Cell(bool(int(elem))) for elem in fin.readline().split()]


    def draw(self, display, cell_size):
        color_green = Color('green')
        color_white = Color('white')
        for i in range(self.nrow):
            for j in range(self.ncol):
                draw.rect(display, 
                          color_green if self.grid[i][j].is_alive() 
                          else color_white,
                          (cell_size * i + 1, cell_size * j + 1,
                          cell_size, cell_size))


    def update(self):
        pass


    def __iter__(self):
        pass


    def __next__(self):
        pass


    def __str__(self):
        pass


    def __repr__(self):
        pass    


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 200):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed
        
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)
        
        self.cell_width = (width // cell_size)
        self.cell_height = (height // cell_size)


    def cell_list(self, randomize=False):
        self.grid = [[random.randint(0, 1) * (randomize == True)
                      for j in range(self.cell_height)]
                     for i in range(self.cell_width)]
        '''self.grid[0][0] = 1
        self.grid[1][0] = 1
        self.grid[2][0] = 1
        self.grid[2][1] = 1
        self.grid[1][2] = 1''' # человечек


    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))


    def get_neighbours(self, cell):
        count = 0
        for (i, j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), 
                     (1, 0), (1, 1)]:
            if (self.grid[(cell[0] + i) % self.cell_width]
                [(cell[1] + j) % self.cell_height] == True):
                count += 1
        return count
    
    
    def update_cell_list(self):
        ans_grid = list()
        for i in range(self.cell_width):
            ans_grid.append(list())
            for j in range(self.cell_height):
                neighbours = self.get_neighbours((i, j))
                if 2 <= neighbours <= 3 and self.grid[i][j] == True:
                    ans_grid[-1].append(True)
                elif neighbours == 3 and self.grid[i][j] == False:
                    ans_grid[-1].append(True)
                else:
                    ans_grid[-1].append(False)
        self.grid = ans_grid


    def draw_cell_list(self):
        color_green = Color('green')
        color_white = Color('white')
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                draw.rect(self.screen, 
                          color_green if self.grid[i][j] else color_white,
                          (self.cell_size * i + 1, self.cell_size * j + 1,
                          self.cell_size, self.cell_size))


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.cell_list(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
            self.update_cell_list()
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(1200, 700, 5)
    game.run()
