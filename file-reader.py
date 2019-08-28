import curses
from os.path import abspath
import sys
from time import sleep


class FileText:
    """An object to represent the text being displayed on the screen"""

    def __init__(self, lines, cols):
        # access current char in grid by grid[x][y]
        self.grid = [[' ' for _ in range(lines)] for _ in range(cols)]

    def replace(self, x, y, char):
        """replaces one char in the canvas at location (x, y)"""
        self.grid[x][y] = char

    def display(self, lines_start, lines_stop, cols_start, cols_stop):
        """Displays a certain section of the text"""
        transposed = [[col[i] for col in self.grid[cols_start:cols_stop]]
                      for i in list(range(len(self.grid[0])))[lines_start:lines_stop]]
        return '\n'.join([''.join(line) for line in transposed])


def main(stdscr, file):

    # read file
    with open(abspath(file), 'r') as f:
        file_contents = f.read()
    
    # create FileText object with grid size exactly large enough to display entire file contents
    file_lines = file_contents.split('\n')
    dims = [len(file_lines), max([len(line) for line in file_lines])]
    file_text = FileText(*dims)

    for y, line in enumerate(file_lines):
        for x, char in enumerate(line):
            file_text.replace(x, y, char)

    lines_start = 0
    lines_stop = curses.LINES - 1
    cols_start = 0
    cols_stop = curses.COLS - 1

    stdscr.nodelay(True)
    key = ""
    while True:
        try:
            key = stdscr.getkey()
            if str(key) == "q":
                sys.exit()
        except Exception:
            # no input
            pass
        stdscr.clear()
        stdscr.addstr(file_text.display(lines_start, lines_stop, cols_start, cols_stop))
        stdscr.refresh()
        
        sleep(0.01)


if __name__ == "__main__":

    file = sys.argv[1]

    curses.wrapper(main, file)