import curses
import curses.textpad
from os.path import abspath, dirname, isfile
import os
import sys
import time
import signal
import random

from separate_mainloops import (
    ask_to_quit, find_in_file, 
    sign_up_prompt, FileText,
    compile_screen, popup)


CWD = dirname(abspath(__file__))
ASCII_DIR = CWD + '/ascii-art'
POPUPS = ['ascii-art/popups/' + i for i in os.listdir(ASCII_DIR + '/popups')]


def convert_to_binary(i, byte_size):
    binary = bin(i)[2:]
    zeroes = ''.join(['0' for _ in range(byte_size - len(binary))])
    return zeroes + binary


def main(stdscr, file):

    # catch ^c
    def signal_handler(sig, frame):
        pass
    signal.signal(signal.SIGINT, signal_handler)

    stdscr.nodelay(1)
    lines_start = 0
    lines_stop = curses.LINES
    cols_start = 0
    cols_stop = curses.COLS - 1

    # ask for encoding
    while True:
        key = stdscr.getch()

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, curses.LINES, curses.COLS, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, curses.LINES, curses.COLS, 10, True)

        elif key == 97:  # a
            encoding = 'utf-16'
            break

        elif key == 98:  # b
            encoding = 'ascii'
            break

        elif key == 99:  # c
            encoding = 'utf-8'
            break
        
        stdscr.clear()
        try:
            stdscr.addstr("What encoding would you like to open this file in?\n\
(If the file can not be read with that encoding, it will be displayed in binary)\n\
UTF-16 [a]\tASCII [b]\tUTF-8 [c]")
        except Exception:
            raise Exception("Terminal window is too small")
        stdscr.refresh()
        time.sleep(0.01)

    # ask to open in browser
    while True:
        key = stdscr.getch()

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, curses.LINES, curses.COLS, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, curses.LINES, curses.COLS, 10, True)
        
        elif key == 121:  # y
            os.system(f'open -a "Google Chrome" {abspath(file)}')
            break
        
        elif key == 110:  # n
            break

        stdscr.clear()
        try:
            stdscr.addstr('Would you like to open your file in your webbrowser as well? [y/n]')
        except Exception:
            raise Exception('Terminal window is too small')

        stdscr.refresh()
        time.sleep(0.01)

    # ask what language to compile in
    while True:
        key = stdscr.getch()

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, curses.LINES, curses.COLS, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, curses.LINES, curses.COLS, 10, True)

        elif key == 99:  # c
            compile_screen(stdscr, file, curses.LINES, curses.COLS)
            break

        elif key == 114:  # r
            break

        stdscr.clear()
        try:
            stdscr.addstr('Would you like to compile this file as well?\nCompile [c]\tJust Read [r]')
        except Exception:
            raise Exception('Terminal window is too small')

        stdscr.refresh()
        time.sleep(0.01)

    # display sign up screen if file size is over 1 kb
    if os.stat(abspath(file)).st_size > 1000:
        with open(ASCII_DIR + '/sign-up.txt', 'r') as f:
            popup_contents = f.read()
        popup_lines = popup_contents.split('\n')

        dims = [len(popup_lines), max([len(line) for line in popup_lines])]
        popup_text = FileText(*dims, popup_contents)
        
        for y, line in enumerate(popup_lines):
            for x, char in enumerate(line):
                popup_text.replace(x, y, char)

        sign_up_prompt(stdscr, curses.LINES, curses.COLS, popup_text,
                       lines_start, lines_stop, cols_start, cols_stop)

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
    
    dims = [len(file_lines), max([len(line) for line in file_lines]) + 1]
    file_text = FileText(*dims, file_contents)

    for y, line in enumerate(file_lines):
        for x, char in enumerate(line):
            file_text.replace(x, y, char)

    add_x = 0
    add_y = 0

    # list contains 1000 items and only 1 of them is True.
    # Meaning that a popup should come about every 10 seconds.
    popup_or_no = [True] + [False for _ in range(999)]

    # main mainloop (for actually viewing file contents)
    while True:
        
        if random.choice(popup_or_no):
            popup(stdscr, random.choice(POPUPS), curses.LINES, curses.COLS)

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
        
        elif key == 2:  # ^b (compile)
            compile_screen(stdscr, file, curses.LINES, curses.COLS)

        elif key == 20: # ^t (find in file)
            find_in_file(stdscr, curses.LINES, curses.COLS,
                         lines_start, lines_stop, cols_start, cols_stop, file_text)
        
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
        try:
            stdscr.addstr(file_text.display(lines_start, lines_stop,
                                            cols_start, cols_stop))
        except Exception:
            raise Exception('Terminal window is too small')

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

    try:
        ipt = sys.argv[1]
    except IndexError:
        print('No input file specified. Use -h flag for more information on usage.')
        sys.exit()

    if ipt == '-h':
        help_screen = True
    else:
        file = ipt
        help_screen = False

    if help_screen:
        os.system("less helpscreen")
        sys.exit()

    curses.wrapper(main, file)