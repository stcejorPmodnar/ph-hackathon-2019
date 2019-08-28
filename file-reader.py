import curses
import sys
from time import sleep


class Canvas:
    """An object to represent the text being displayed on the screen"""

    def __init__(self, lines, cols):
        # access current char in grid by grid[x][y]
        self.grid = [[' ' for _ in range(lines)] for _ in range(cols)]

    def replace(self, x, y, char):
        """replaces one char in the canvas at location (x, y)"""
        self.grid[x][y] = char

    @property
    def display(self):
        transposed = [[col[i] for col in cols] for i in range(len(self.grid(0)))]
        return '\n'.join([' '.join(line) for line in transposed])
