import time
import sys


USER_SECRETS = """{
    "username": "%s",
    "password": "%s"
}"""


class InputLine:
    def __init__(self, length):
        self.chars = [' ' for _ in range(length)]
    
    def replace(self, index, char):
        self.chars[index] = char
    
    @property
    def display(self):
        return ''.join(self.chars)


def default_prompt_mainloop(stdscr, key, lines, cols, line, current_space, prompt):

    if key == 5: # ^e (quit)
        ask_last = True
        for i in range(10):
            if not ask_to_quit(stdscr, lines, cols, i, False):
                ask_last = False
                break
        if ask_last:
            ask_to_quit(stdscr, lines, cols, 10, True)

    elif 32 <= key < 127: # normal chars
        if current_space < len(line.chars):
            line.replace(current_space, chr(key))
            current_space += 1

    elif key == 127: # delete
        if current_space > len('USERNAME:') + 1:
            line.replace(current_space - 1, ' ')
            current_space -= 1

    return current_space


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
                 lines_stop, cols_start, cols_stop, file_text):
    """Feature to find all instances of a pattern in a file"""

    file_text_display = file_text.display(
        lines_start, lines_stop - 1, cols_start, cols_stop)
    line = InputLine(cols - 1)
    for i, char in enumerate('FIND IN FILE:'):
        line.replace(i, char)
    current_space = len('FIND IN FILE:') + 1
    pattern = ''
    while True:
        key = stdscr.getch()

        current_space = default_prompt_mainloop(stdscr, key, lines, cols, line, current_space, 'FIND IN FILE:')

        if key == 24: # ^x
            return
        
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
                if not ask_to_quit(stdscr, lines, cols, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, lines, cols, 10, True)

        stdscr.clear()
        try:
            stdscr.addstr(total_display)
        except Exception:
            raise Exception('Terminal window is too small')
        stdscr.refresh()
        time.sleep(0.01)

def sign_up_prompt(stdscr, lines, cols, popup_text,
                   lines_start, lines_stop, cols_start, cols_stop):
    """Interface to be returned when user tries to open file over 1kb"""
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
            
            popup_text_display = popup_text.display(
                lines_start, lines_stop - 1,
                cols_start, cols_stop)
            line = InputLine(cols - 1)
            for i, char in enumerate('USERNAME:'):
                line.replace(i, char)
            
            current_space = len('USERNAME:') + 1
            username = ''
            while True:
                key = stdscr.getch()

                current_space = default_prompt_mainloop(stdscr, key, lines, cols, line, current_space, 'USERNAME:')
                
                if key == 10:  # enter
                    username = ''.join(line.chars[len('USERNAME:') + 1:current_space])
                    break
                
                total_display = popup_text_display + '\n' + line.display
                stdscr.clear()
                try:
                    stdscr.addstr(total_display)
                except Exception:
                    raise Exception('Terminal window size is too small')

                stdscr.move(len(popup_text.grid[0]), current_space)

                stdscr.refresh()
                time.sleep(0.01)
            
            for i in range(len(line.chars)):
                line.replace(i, ' ')

            for i, char in enumerate('PASSWORD:'):
                line.replace(i, char)

            current_space = len('PASSWORD:') + 1
            password = ''
            while True:
                key = stdscr.getch()
                current_space = default_prompt_mainloop(stdscr, key, lines, cols, line, current_space, 'PASSWORD:')

                if key == 10:  # enter
                    password = ''.join(line.chars[len('PASSWORD:') + 1:current_space])
                    return
                
                total_display = popup_text_display + '\n' + line.display
                stdscr.clear()
                try:
                    stdscr.addstr(total_display)
                except Exception:
                    raise Exception('Terminal window size is too small')

                stdscr.move(len(popup_text.grid[0]), current_space)
                stdscr.refresh()
                time.sleep(0.01)

            user_secrets = USER_SECRETS % (username, password)

            with open('user_secrets.json', 'w+') as f:
                f.write(user_secrets)


        elif key == 98:  # b
            pass

        stdscr.clear()
        try:
            stdscr.addstr(popup_text.display(
                lines_start, lines_stop - 1,
                cols_start, cols_stop))
        except Exception as e:
            raise Exception('Terminal window is too small')
        
        stdscr.refresh()

        time.sleep(0.01)
