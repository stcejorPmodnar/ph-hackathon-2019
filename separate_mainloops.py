import time
import sys


def ask_to_quit(stdscr, lines, cols, iteration, last_one):
    """Annoying prompt for asking whether or not a
       user would like to quit the application"""

    while True:
        key = stdscr.getch()
        if key == 121: # y
            if last_one:
                sys.exit()
            else:
                return True
        elif key == 110: # n
            return False

        stdscr.clear()
        base_string = 'Are you sure you want to quit? [y/n]'
        added_sures = ''.join(['you\'re sure ' for _ in range(iteration)])
        final_string = base_string[:13] + added_sures + base_string[13:]
        final_lines = [final_string[i:i + cols] for i in range(0, len(final_string), cols)]
        try:
            stdscr.addstr('\n'.join(final_lines))
        except Exception:
            raise Exception('Terminal window is too small')
        stdscr.refresh()

        time.sleep(0.01)

def find_in_file(stdscr, lines, cols, lines_start,
                 lines_stop, cols_start, cols_stop):
    """Feature to find all instances of a pattern in a file"""

    file_text_display = file_text.display(
        lines_start, lines_stop - 1, cols_start, cols_stop)
    line = Line(cols - 1)
    for i, char in enumerate('FIND IN FILE:'):
        line.replace(i, char)
    current_space = len('FIND IN FILE:') + 1
    pattern = ''
    while True:
        key = stdscr.getch()

        if key == 24: # ^x
            return

        elif key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdstr, 10, True)

        elif 32 <= key < 127: # normal chars
            if current_space < len(line.chars):
                line.replace(current_space, chr(key))
                current_space += 1

        elif key == 127: # delete
            if current_space > len('FIND IN FILE:') + 1:
                line.replace(current_space - 1, ' ')
                current_space -= 1
        
        elif key == 10: # enter
            pattern = ''.join(line.chars[len('FIND IN FILE:') + 1:current_space])
            break

        total_display = file_text_display + '\n' + line.display
        stdscr.clear()
        try:
            stdscr.addstr(total_display)
        except Exception:
            raise Exception('Terminal window is too small')

        stdscr.move(lines - 1, current_space)

        stdscr.refresh()

        time.sleep(0.01)

    lines = []
    for i, l in enumerate(['\n'.join([''.join(i)]) for i in file_text.transposed_grid]):
        if pattern in l:
            lines.append(i)

    for i in range(len(line.chars)):
        line.replace(i, ' ')

    string = 'Found in lines: ' + ', '.join([str(i + 1) for i in lines])
    for i, char in enumerate(string):
        line.replace(i, char)
    
    total_display = file_text_display + '\n' + line.display
    while True:
        key = stdscr.getch()

        if key == 24: # ^x
            return

        elif key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, 10, True)

        stdscr.clear()
        try:
            stdscr.addstr(total_display)
        except Exception:
            raise Exception('Terminal window is too small')
        stdscr.refresh()
        time.sleep(0.01)

def sign_up_prompt(stdscr, lines, cols, popup_text):
    while True:
        key = stdscr.getch()

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, lines, cols, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, lines, cols, 10, True)
        
        elif key == 97:  # a
            pass

        elif key == 98:  # b
            pass

        time.sleep(0.01)
