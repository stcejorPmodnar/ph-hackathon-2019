import curses
import curses.textpad
from os.path import abspath, isfile
import os
import sys
import time


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


class Line:
    def __init__(self, length):
        self.chars = [' ' for _ in range(length)]
    
    def replace(self, index, char):
        self.chars[index] = char
    
    @property
    def display(self):
        return ''.join(self.chars)


def main(stdscr, file):
    
    def ask_to_quit(iteration, last_one):

        while True:   
            key = stdscr.getch()
            if key == 121: # y
                if last_one:
                    sys.exit()
                else:
                    return
            elif key == 110: # n
                pass

            stdscr.clear()
            base_string = 'Are you sure you want to quit? [y/n]'
            added_sures = ''.join(['you\'re sure ' for _ in range(iteration)])
            final_string = base_string[:13] + added_sures + base_string[13:]
            stdscr.addstr(final_string)
            stdscr.refresh()

            time.sleep(0.01)

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
    lines_stop = curses.LINES
    cols_start = 0
    cols_stop = curses.COLS - 1

    add_x = 0
    add_y = 0

    stdscr.nodelay(1)
    while True:
        
        x_changed = False
        y_changed = False

        key = stdscr.getch()
        
        if key != -1:
            with open('output', 'w') as f:
                f.write(str(key))

        if key == 5: # ^e (quit)
            for i in range(10):
                ask_to_quit(i, False)
            ask_to_quit(10, True)
        
        elif key == 117: # u
            add_y -= 1
            y_changed = True
        elif key == 100: # d
            add_y += 1
            y_changed = True
        elif key == 114: # r
            add_x += 1
            x_changed = True
        elif key == 108: # l
            add_x -= 1
            x_changed = True

        stdscr.clear()
        stdscr.addstr(file_text.display(lines_start, lines_stop, cols_start, cols_stop))

        # move cursor
        y, x = stdscr.getyx()
        new_x = x + add_x
        new_y = y + add_y
        if x_changed:
            if new_x >= curses.COLS:
                # scroll if possible
                if len(file_text.grid) >= new_x:
                    cols_start += 1
                    cols_stop += 1
                add_x -= 1
                new_x -= 1
            elif new_x < 0:
                if cols_start > 0:
                    cols_start -= 1
                    cols_stop -= 1
                add_x += 1
                new_x += 1
        elif y_changed:
            if new_y > curses.LINES:
                # scroll if possible
                if len(file_text.grid[0]) >= new_y:
                    lines_start += 1
                    lines_stop += 1
                add_y -= 1
                new_y -= 1
            elif new_y < 0:
                if lines_start > 0:
                    lines_start -= 1
                    lines_stop -= 1
                add_y += 1
                new_y += 1
        
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
        encoding = "binary"
    
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

    curses.wrapper(main, file)