"""
Maze Solver by Luca Zani
https://github.com/ZaniLuca/MazeSolver
made following TheCodingTrain tutorials
https://www.youtube.com/user/shiffman
"""
import pygame
from Cell import Cell
from Colors import *

pygame.init()


class Game:

    def __init__(self):
        self.width = 400
        self.height = 400
        self.w = 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 30
        self.grid = [[None for i in range(self.width // self.w)] for j in
                     range(self.height // self.w)]
        self.stack = []
        self.done = False

        pygame.display.set_caption("Maze Generator")

    def run(self):
        """
        Game loop
        :return: None
        """
        clock = pygame.time.Clock()
        self.createGrid()
        current = self.grid[0][0]

        run = True
        while run:
            clock.tick(self.fps)

            if not self.done:
                current.visited = True
                current.highlight(self.screen, self.w)
                pygame.display.update()
                next_cell = current.checkNeighbors(self.grid, self.width // self.w, self.height // self.w)

                if next_cell:
                    next_cell.visited = True
                    self.removeWalls(current, next_cell)
                    self.stack.append(current)

                    current = next_cell

                elif len(self.stack) > 0:
                    current = self.stack.pop()
                else:
                    self.done = True
            else:
                pass
                #Solve

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.update()
        pygame.quit()

    def update(self):
        """
        updates the screen
        draw everything
        :return: None
        """
        self.screen.fill(white)
        for i in range(self.width // self.w):
            for j in range(self.height // self.w):
                self.grid[i][j].show(self.screen, self.w)
        pygame.display.flip()

    def createGrid(self):
        """
        create the grid
        :return: None
        """

        for i in range(self.width // self.w):  # Cols
            for j in range(self.height // self.w):  # Rows
                self.grid[i][j] = Cell(i, j)

    def removeWalls(self, a, b):
        """
        removes a wall between a and b
        :param a: Cell
        :param b: Cell
        :return: None
        """
        x = a.i - b.i
        if x == 1:
            a.walls[3] = False
            b.walls[1] = False
        elif x == -1:
            a.walls[1] = False
            b.walls[3] = False
        y = a.j - b.j
        if y == 1:
            a.walls[0] = False
            b.walls[2] = False
        elif y == -1:
            a.walls[2] = False
            b.walls[0] = False


g = Game()
g.run()
