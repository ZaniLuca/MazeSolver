"""
Maze Solver by Luca Zani
https://github.com/ZaniLuca/MazeSolver
made following TheCodingTrain tutorials
https://www.youtube.com/user/shiffman
"""
import pygame
import math
from Cell import Cell
from Colors import *

pygame.init()
pygame.display.init()


class Game:

    def __init__(self):
        self.width = 800
        self.height = 800
        self.w = 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.grid = [[None for i in range(self.width // self.w)] for j in
                     range(self.height // self.w)]
        self.stack = []
        self.generated = False
        self.solved = False
        self.start = None
        self.end = None
        self.openSet = []
        self.closedSet = []
        self.path = []

        pygame.display.set_caption("Maze Solver")

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

            if not self.generated:
                current.visited = True
                current.highlight(self.screen, self.w)
                pygame.display.update()
                next_cell = current.randomNeighbor(self.grid, self.width // self.w, self.height // self.w)

                if next_cell:
                    next_cell.visited = True
                    self.removeWalls(current, next_cell)
                    self.stack.append(current)

                    current = next_cell

                elif len(self.stack) > 0:
                    current = self.stack.pop()
                else:
                    self.generated = True
                    self.start = self.grid[0][0]
                    self.end = self.grid[self.width // self.w - 1][self.height // self.w - 1]
                    self.openSet.append(self.start)
            else:
                # Solving
                if not self.solved:
                    if len(self.openSet) > 0:
                        best = 0  # Index of the lowest F cell
                        for i in range(len(self.openSet)):
                            if self.openSet[i].f < self.openSet[best].f:
                                best = i

                        current = self.openSet[best]

                        # Win Condition
                        if self.openSet[best] == self.end:
                            temp = current
                            self.path.append(temp)
                            while temp.previous:
                                self.path.append(temp.previous)
                                temp = temp.previous

                            self.solved = True
                            print('Done!')

                        self.openSet.remove(current)
                        self.closedSet.append(current)

                        # Evaluating neighbors
                        for i in range(len(current.neighbors)):
                            neighbor = current.neighbors[i]

                            if neighbor not in self.closedSet:
                                canGo = False
                                pos = self.checkPosition(current, neighbor)

                                if pos == 'top' and not current.walls[0]:
                                    canGo = True
                                elif pos == 'right' and not current.walls[1]:
                                    canGo = True
                                elif pos == 'bottom' and not current.walls[2]:
                                    canGo = True
                                elif pos == 'left' and not current.walls[3]:
                                    canGo = True

                                # if pos == 'top_right' and not current.walls[0] and not current.walls[1]:
                                #     canGo = True
                                # elif pos == 'bottom_right' and not current.walls[2] and not current.walls[1]:
                                #     canGo = True
                                # elif pos == 'top_left' and not current.walls[0] and not current.walls[3]:
                                #     canGo = True
                                # elif pos == 'bottom_left' and not current.walls[2] and not current.walls[3]:
                                #     canGo = True

                                if canGo:
                                    temp_g = current.g + 1
                                    # Check if i have evaluated the neighbor before
                                    # if so we have a better G score
                                    if neighbor in self.openSet:
                                        if temp_g < neighbor.g:
                                            neighbor.g = temp_g
                                    # otherwise just give the neighbor the temp_g
                                    else:
                                        neighbor.g = temp_g
                                        self.openSet.append(neighbor)

                                    neighbor.h = self.heuristic(neighbor)
                                    neighbor.f = neighbor.g + neighbor.h
                                    neighbor.previous = current

                    else:
                        print('No Solution')

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
                self.grid[i][j].show(self.screen, self.w, grey, 0)
        if self.generated:
            # OpenSet
            for i in range(len(self.openSet)):
                self.openSet[i].show(self.screen, self.w, blue, 12)

            # ClosedSet
            for i in range(len(self.closedSet)):
                self.closedSet[i].show(self.screen, self.w, red, 12)

            # Path
            for i in range(len(self.path)):
                self.path[i].show(self.screen, self.w, green, 10)

            self.end.show(self.screen, self.w, yellow, 1)
            self.start.show(self.screen, self.w, yellow, 1)
        pygame.display.flip()

    def createGrid(self):
        """
        create the grid
        :return: None
        """

        for i in range(self.width // self.w):  # Cols
            for j in range(self.height // self.w):  # Rows
                self.grid[i][j] = Cell(i, j)

        # Adds Neighbors
        for i in range(self.width // self.w):
            for j in range(self.height // self.w):
                self.grid[i][j].addNeighbors(self.grid, self.width // self.w, self.height // self.w)

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

    def heuristic(self, neighbor):
        """
        Calculate the h cost from the neighbor to the end
        h cost = distance from neighbir --> end
        :param neighbor: Cell
        :return: double
        """
        distance = math.sqrt((neighbor.i - self.end.i) ** 2 + (neighbor.j - self.end.j) ** 2)
        return distance

    def checkPosition(self, a, b):
        """
        check where B is based on A
        :param a: cell
        :param b: cell
        :return: string
        """
        # Horizontal
        if b.i > a.i:
            return 'right'
        elif b.i < a.i:
            return 'left'
        # Vetical
        if b.j > a.j:
            return 'bottom'
        elif b.j < a.j:
            return 'top'


g = Game()
g.run()
