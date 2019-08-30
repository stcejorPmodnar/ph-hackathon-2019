import curses
import curses.textpad
from os.path import abspath, dirname, isfile
import os
import sys
import time
import signal

from separate_mainloops import ask_to_quit, find_in_file, sign_up_prompt


CWD = dirname(abspath(__file__))
ASCII_DIR = CWD + '/ascii-art'


def convert_to_binary(i, byte_size):
    binary = bin(i)[2:]
    zeroes = ''.join(['0' for _ in range(byte_size - len(binary))])
    return zeroes + binary


class FileText:
    """An object to represent the text being displayed on the screen"""

    def __init__(self, lines, cols):
        # access current char in grid by grid[x][y]
        self.grid = [[' ' for _ in range(lines)] for _ in range(cols)]

    @property
    def transposed_grid(self):
        return [[col[i] for col in self.grid] for i in range(len(self.grid[0]))]

    def replace(self, x, y, char):
        """replaces one char in the canvas at location (x, y)"""
        self.grid[x][y] = char

    def display(self, lines_start, lines_stop, cols_start, cols_stop):
        """Displays a certain section of the text"""
        transposed = [[col[i] for col in self.grid[cols_start:cols_stop]]
                      for i in list(range(len(self.grid[0])))[lines_start:lines_stop]]
        return '\n'.join([''.join(line) for line in transposed])


class Line:
    def __init__(self, length):
        self.chars = [' ' for _ in range(length)]
    
    def replace(self, index, char):
        self.chars[index] = char
    
    @property
    def display(self):
        return ''.join(self.chars)


def main(stdscr, file, encoding, color):

    # catch ^c
    def signal_handler(sig, frame):
        pass
    signal.signal(signal.SIGINT, signal_handler)

    stdscr.nodelay(1)
    lines_start = 0
    lines_stop = curses.LINES
    cols_start = 0
    cols_stop = curses.COLS - 1

    # display sign up screen if file size is over 1 kb
    if os.stat(abspath(file)).st_size > 1000:
        with open(ASCII_DIR + '/email.txt', 'r') as f:
            popup_contents = f.read()
        popup_lines = popup_contents.split('\n')

        dims = [len(file_lines), max([len(line) for line in file_lines])]
        popup_text = FileText(*dims)
        
        for y, line in enumerate(popup_lines):
            for x, char in enumerate(line):
                popup_text.replace(x, y, char)

        sign_up_prompt(stdscr, curses.LINES, curses.COLS, popup_text)

    # read file
    binary = False
    try:
        with open(abspath(file), 'r', encoding=encoding) as f:
            file_contents = f.read()
    except UnicodeDecodeError:
        with open(abspath(file), 'rb') as f:
            file_contents = ' '.join(convert_to_binary(i, 16) for i in list(f.read()))
        binary = True

    
    # create FileText object with grid size exactly large enough to display entire file contents
    if binary:
        file_lines = [file_contents[i:i + curses.COLS - 1]
                    for i in range(0, len(file_contents), curses.COLS - 1)]
    else:
        file_lines = file_contents.split('\n')
    
    dims = [len(file_lines), max([len(line) for line in file_lines])]
    file_text = FileText(*dims)

    for y, line in enumerate(file_lines):
        for x, char in enumerate(line):
            file_text.replace(x, y, char)

    add_x = 0
    add_y = 0

    while True:
        
        x_changed = False
        y_changed = False

        key = stdscr.getch()

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, curses.LINES, curses.COLS, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, curses.LINES, curses.COLS, 10, True)
        
        elif key == 20: # ^t (find in file)
            find_in_file(stdscr, curses.LINES, curses.COLS,
                         lines_start, lines_stop, cols_start, cols_stop)
        
        elif key == 259: # up arrow
            add_y -= 1
            y_changed = True
        elif key == 258: # down arrow
            add_y += 1
            y_changed = True
        elif key == 261: # right arrow
            add_x += 1
            x_changed = True
        elif key == 260: # left arrow
            add_x -= 1
            x_changed = True

        stdscr.clear()
        stdscr.addstr(file_text.display(lines_start, lines_stop, cols_start, cols_stop))

        # move cursor
        move = True
        y, x = stdscr.getyx()
        new_x = x + add_x
        new_y = y + add_y
        if x_changed:
            if new_x >= curses.COLS:
                # scroll if possible
                if len(file_text.grid) > (cols_start + new_x):
                    cols_start += 1
                    cols_stop += 1
                    add_x -= 1
                    new_x -= 1
                else:
                    move = False
                    add_x -= 1
                    new_x -= 1
            elif new_x < 0:
                if cols_start > 0:
                    cols_start -= 1
                    cols_stop -= 1
                add_x += 1
                new_x += 1
        elif y_changed:
            if new_y > curses.LINES - 1:
                # scroll if possible
                if len(file_text.grid[0]) > (lines_start + new_y):
                    lines_start += 1
                    lines_stop += 1
                    add_y -= 1
                    new_y -= 1
                else:  # if cursor wants to go beyond file contents
                    move = False
                    add_y -= 1
                    new_y -= 1
            elif new_y < 0:
                if lines_start > 0:
                    lines_start -= 1
                    lines_stop -= 1
                add_y += 1
                new_y += 1
        
        if move:
            stdscr.move(new_y, new_x)

        stdscr.refresh()

        time.sleep(0.01)

if __name__ == "__main__":


    for i in range(len(sys.argv) - 1):
        if (sys.argv[i + 1] == "-h" and sys.argv[i + 2] == "-e" and sys.argv[i + 3] == "-l"
                and sys.argv[i + 4] == "-p" and sys.argv[i + 5] == "-m" and sys.argv[i + 6] == "-e"):
            helpScreen = True
        elif sys.argv[i + 1] == "-e" and sys.argv[i] != "-h" and sys.argv[i] != "-m":
            encoding = sys.argv[i + 2]
        elif sys.argv[i + 1] == "-c":
            color = sys.argv[i + 2]
        elif isfile(sys.argv[i + 1]):
            file = sys.argv[i + 1]

    try: color
    except NameError:
        color = "rainbow"

    try: encoding
    except NameError:
        encoding = "utf-16"
    
    try: helpScreen
    except NameError:
        helpScreen = False

    try: file
    except NameError:
        print("Specify a file to be read.")
        sys.exit()

    if helpScreen:
        os.system("less helpscreen")
        sys.exit()

    curses.wrapper(main, file, encoding, color)