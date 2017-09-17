import pygame
import random
from pygame import *


class Cell:
    def __init__(self, state, i, j):
        self.state = state
        self.i = i
        self.j = j

    def set_state(self, state):
        self.state = state

    def is_alive(self):
        return self.state

    def __str__(self):
        return '1' if self.state else '0'


class CellList:
    def __init__(self, nrow=10, ncel=10, filename=None):
        self.nrow = nrow
        self.ncel = ncel
        self.filename = filename
        self.irow = 0
        self.icel = -1

        self.grid = list()
        for i in range(self.nrow):
            self.grid.append(list())
            for j in range(self.ncel):
                self.grid[-1].append(Cell(0, i, j))

        if filename is not None:
            fin = open(filename)
            for i in range(nrow):
                line = fin.readline().split()
                grid[i] = [Cell(bool(int(line[j])), i, j)
                           for j in range(len(line))]
            fin.close()

    def get_neighbours(self, cell):
        count = 0
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]
        for i, j in moves:
            if (self.grid[(cell[0] + i) % self.nrow][(cell[1] + j) %
                                                     self.ncel].is_alive()):
                count += 1
        return count

    def update(self):
        ans_grid = list()
        for i in range(self.nrow):
            ans_grid.append(list())
            for j in range(self.ncel):
                ans_grid[-1].append(Cell(0, i, j))
        for i in range(self.nrow):
            for j in range(self.ncel):
                neighbours = self.get_neighbours((i, j))
                if 2 <= neighbours <= 3 and self.grid[i][j].is_alive():
                    ans_grid[i][j].set_state(True)
                elif neighbours == 3 and not self.grid[i][j].is_alive():
                    ans_grid[i][j].set_state(True)
                else:
                    ans_grid[i][j].set_state(False)
        self.grid = ans_grid

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self.grid[key[0]][key[1]]

    def __next__(self):
        self.icel += 1
        if self.icel == self.ncel:
            self.icel = 0
            self.irow += 1
        if self.irow == self.nrow:
            raise StopIteration
        return self.grid[0][0]

    def __str__(self):
        ans = '[[' + ', '.join([str(elem.state)
                                for elem in self.grid[0]]) + '],\n'
        for i in range(self.nrow - 1):
            ans += ' [' + ', '.join([str(elem.state)
                                     for elem in self.grid[i]]) + '],\n'
        ans += ' [' + ', '.join([str(elem.state)
                                 for elem in self.grid[-1]]) + ']]'
        return ans


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=1):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed

        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = (width // cell_size)
        self.cell_height = (height // cell_size)

    def cell_list(self, randomize=False):
        self.grid = CellList(self.cell_width, self.cell_height, None)
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                self.grid[(i, j)].set_state(random.randint(0, 1))
        print(self.grid)

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def update_cell_list(self):
        self.grid.update()

    def draw_cell_list(self):
        color_green = Color('green')
        color_white = Color('white')
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                draw.rect(self.screen, color_green
                          if self.grid[(i, j)].is_alive() else color_white,
                          (self.cell_size * self.grid[(i, j)].i + 1,
                           self.cell_size * self.grid[(i, j)].j + 1,
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
