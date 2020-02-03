import random
import pygame
from Colors import *


class Cell:

    def __init__(self, i, j):
        """
        :param i: col
        :param j: row
        """
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.visited = False
        self.f = 0
        self.h = 0
        self.g = 0
        self.neighbors = []
        self.previous = None

    def show(self, screen, w, color, decrement, ispath):
        """
        Shows the walls around the cell
        :param screen: screen
        :param w: int
        :param color: color
        :param decrement: int
        :param ispath: bool
        :return: None
        """
        x = self.i * w
        y = self.j * w

        if self.walls[0]:
            pygame.draw.line(screen, walls, (x, y), (x + w, y), 2)
        if self.walls[1]:
            pygame.draw.line(screen, walls, (x + w, y), (x + w, y + w), 2)
        if self.walls[2]:
            pygame.draw.line(screen, walls, (x + w, y + w), (x, y + w), 2)
        if self.walls[3]:
            pygame.draw.line(screen, walls, (x, y + w), (x, y), 2)

        # if the cell has been visited draw a rectangle in it,
        # otherwise if we want to draw a path --> ispath == True
        # draw a circle

        if self.visited:
            if ispath:
                pygame.draw.circle(screen, color, (x + 2 + w // 2, y + 2 + w // 2), decrement)
            else:
                rect = pygame.Rect(x + 2 + decrement // 2, y + 2 + decrement // 2, w - decrement, w - decrement)
                pygame.draw.rect(screen, color, rect)

    def randomNeighbor(self, grid, cols, rows):
        """
        check every neighbor around the selected cell
        and return a random one
        :param rows: int
        :param cols: int
        :param grid: grid
        :return: random index
        """
        neighbors = []

        top, right, bottom, left = None, None, None, None

        # Here we just make sure that the neighbor we're going to add
        # meets the requirements (example isn't in a wrong spot)
        # and we add it to the temporary array neighbors []

        if self.j > 0:
            top = grid[self.i][self.j - 1]
        if self.i < cols - 1:
            right = grid[self.i + 1][self.j]
        if self.j < rows - 1:
            bottom = grid[self.i][self.j + 1]
        if self.i > 0:
            left = grid[self.i - 1][self.j]

        # we wanna make sure that we haven't already visited
        # the neighbor so we check if it exists and it hasn't been visited

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        # then if there is at least one neighbor in the array we can
        # randomly pick one and return it

        if len(neighbors) > 0:
            return neighbors[int(random.randrange(0, len(neighbors)))]
        else:
            return None

    def addNeighbors(self, grid, cols, rows):
        """
        Adds neighbors for the A* to work
        :param grid: grid
        :param cols: int
        :param rows: int
        :return: None
        """
        # This function is just for the A*

        if self.j > 0:
            self.neighbors.append(grid[self.i][self.j - 1])  # top
        if self.i < cols - 1:
            self.neighbors.append(grid[self.i + 1][self.j])  # right
        if self.j < rows - 1:
            self.neighbors.append(grid[self.i][self.j + 1])  # bottom
        if self.i > 0:
            self.neighbors.append(grid[self.i - 1][self.j])  # left
