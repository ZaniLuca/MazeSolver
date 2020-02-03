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
        self.width = 600
        self.height = 600
        self.w = 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        # Initialize the 2D array
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

        pygame.display.set_icon(pygame.image.load('Logo.ico'))
        pygame.display.set_caption("Maze Solver -- by Luca Zani")

    def run(self):
        """
        Game loop
        :return: None
        """
        clock = pygame.time.Clock()
        self.createGrid()
        # Start creating the maze from the top left corner
        current = self.grid[0][0]

        run = True
        while run:
            clock.tick(self.fps)

            if not self.generated:
                # each step we mark the current cell as visited
                # then we get a random neighbor from the current cell
                # that'll be our next pick

                current.visited = True
                next_cell = current.randomNeighbor(self.grid, self.width // self.w, self.height // self.w)

                # if there is a neighbor we mark it as visited and remove
                # the walls between him and the previous cell (called current)
                # we also put it into the stack to use in case we get stuck
                if next_cell:
                    next_cell.visited = True
                    self.removeWalls(current, next_cell)
                    self.stack.append(current)

                    current = next_cell

                # if we get stack we go back one cell, picking it up from the stack
                elif len(self.stack) > 0:
                    current = self.stack.pop()

                # else if there isn't anything in the stack it means that we reached
                # the end and we are done generating the maze
                # we also set up our start and end point, and put the start point into the open set
                else:
                    self.generated = True
                    self.start = self.grid[0][0]
                    self.end = self.grid[self.width // self.w - 1][self.height // self.w - 1]
                    self.openSet.append(self.start)
            else:
                # if we have already created a maze and it hasn't been solved yet
                # we can start the A* pathfinding
                if not self.solved:
                    if len(self.openSet) > 0:
                        # best is the index of the variable with the lowest F
                        # at start we set it to --> 0
                        best = 0

                        # foreach element in the open set we check what is the lowest in F cost
                        for i in range(len(self.openSet)):
                            if self.openSet[i].f < self.openSet[best].f:
                                best = i

                        # we proceed with only the best cell
                        current = self.openSet[best]

                        # if the best cell is also the end point it means that we reached the end
                        if self.openSet[best] == self.end:
                            temp = current
                            self.path.append(temp)

                            # so we wanna walk back the path from the end to the start
                            while temp.previous:
                                self.path.append(temp.previous)
                                temp = temp.previous

                            self.solved = True
                            print('Done!')

                        # else we haven't reach the end, we remove the current cell from the openSet
                        # and put it into the closedSet
                        self.openSet.remove(current)
                        self.closedSet.append(current)

                        # now we need to proceed into a new cell
                        # we check all the nearby neighbors of the current cell and check if
                        # they exists and aren't already in the closed set
                        for i in range(len(current.neighbors)):
                            neighbor = current.neighbors[i]

                            if neighbor not in self.closedSet:

                                # can_goo means that we can go into that cell and there is no wall
                                # beetween the current cell and the selected neighbor
                                can_go = False
                                pos = self.checkPosition(current, neighbor)

                                if pos == 'top' and not current.walls[0]:
                                    can_go = True
                                elif pos == 'right' and not current.walls[1]:
                                    can_go = True
                                elif pos == 'bottom' and not current.walls[2]:
                                    can_go = True
                                elif pos == 'left' and not current.walls[3]:
                                    can_go = True

                                if can_go:
                                    # if there is no wall we proceed and give the new neighbor the G cost
                                    # from the current cell +1 because we moved one spot
                                    temp_g = current.g + 1

                                    # also we need to check if the neighbor hasn't been evaluated before
                                    # if so we look if the new score is better (low is best)
                                    if neighbor in self.openSet:
                                        if temp_g < neighbor.g:
                                            neighbor.g = temp_g

                                    # otherwise just give the neighbor the temp_g
                                    else:
                                        neighbor.g = temp_g
                                        self.openSet.append(neighbor)

                                    # then we can calculate the H cost and the F cost based on the G and H costs
                                    neighbor.h = self.heuristic(neighbor)
                                    neighbor.f = neighbor.g + neighbor.h

                                    # finally we mark the previous cell from the neighbor
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

        # Grid
        for i in range(self.width // self.w):
            for j in range(self.height // self.w):
                self.grid[i][j].show(self.screen, self.w, bg, 0, False)

        if self.generated:
            if not self.solved:

                # OpenSet
                for i in range(len(self.openSet)):
                    self.openSet[i].show(self.screen, self.w, blue, 12, False)

                # ClosedSet
                for i in range(len(self.closedSet)):
                    self.closedSet[i].show(self.screen, self.w, red, 12, False)

            # Path
            for i in range(len(self.path)):
                self.path[i].show(self.screen, self.w, path, 10, True)

            self.end.show(self.screen, self.w, start_end, 25, False)
            self.start.show(self.screen, self.w, start_end, 25, False)

        pygame.display.flip()

    def createGrid(self):
        """
        create the grid
        :return: None
        """
        # Create every cell
        for i in range(self.width // self.w):  # Cols
            for j in range(self.height // self.w):  # Rows
                self.grid[i][j] = Cell(i, j)

        # and then add every neighbor
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

        # check for the HORIZONTAL position
        if b.i > a.i:
            return 'right'
        elif b.i < a.i:
            return 'left'

        # check for the VERTICAL position
        if b.j > a.j:
            return 'bottom'
        elif b.j < a.j:
            return 'top'


g = Game()
g.run()
