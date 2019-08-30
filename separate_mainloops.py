import time
import sys
import os.path
import string
import json

from encrypt import encrypt, decrypt


USER_SECRETS = '{"username": "%s","password": "%s"}'


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
        if current_space > len(prompt) + 1:
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

        stdscr.move(len(file_text.grid[0]), current_space)

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

    def ask_for_user_secrets(validation=None):
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
                raise Exception('Terminal window is too small')

            stdscr.move(len(popup_text.grid[0]), current_space)

            stdscr.refresh()
            time.sleep(0.01)
        
        for i in range(len(line.chars)):
            line.replace(i, ' ')

        for i, char in enumerate('PASSWORD:'):
            line.replace(i, char)

        current_space = len('PASSWORD:') + 1
        password = ''
        entered_password_chars = []
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

            elif 32 <= key < 127: # normal chars
                if current_space < len(line.chars):
                    line.replace(current_space, '*')
                    entered_password_chars.append(chr(key))
                    current_space += 1

            elif key == 127: # delete
                if current_space > len('PASSWORD:') + 1:
                    line.replace(current_space - 1, ' ')
                    current_space -= 1

            if key == 10:  # enter
                password = ''.join(entered_password_chars)
                if validation:
                    validation_output = validation(password)
                    if validation_output != 'good':
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
                            stdscr.clear()
                            try:
                                stdscr.addstr(validation_output + '\nPress ^e to exit the program.')
                            except Exception:
                                raise Exception('Terminal window is too small')
                break
            
            total_display = popup_text_display + '\n' + line.display
            stdscr.clear()
            try:
                stdscr.addstr(total_display)
            except Exception:
                raise Exception('Terminal window is too small')

            stdscr.move(len(popup_text.grid[0]), current_space)
            stdscr.refresh()
            time.sleep(0.01)

        user_secrets = USER_SECRETS % (username, encrypt(password))

        return user_secrets

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
            def validate_password(password):
                PASSWORD_MESSAGE = """Invalid password. Password must:
 - contain at least one capital letter
 - contain at least one digit
 - contain at least one character that is neither a letter nor a number
 - be at least 10 characters long
 - have at least one character that is repeated more than once
 - not have any whitespace"""
                if set(password) & set(string.ascii_uppercase) == set():
                    return PASSWORD_MESSAGE

                if set(password) & set(string.digits) == set():
                    return PASSWORD_MESSAGE

                if set(password) & set(string.digits + string.ascii_letters) == set():
                    return PASSWORD_MESSAGE

                if len(password) < 10:
                    return PASSWORD_MESSAGE

                char_occurrences = {}
                for char in password:
                    if char not in char_occurrences.keys():
                        char_occurrences[char] = len([i for i in password if i == char])
                no_repeats = True
                for count in char_occurrences.values():
                    if count > 1:
                        no_repeats = False
                        break
                if no_repeats:
                    return PASSWORD_MESSAGE

                return 'good'

            user_secrets = ask_for_user_secrets(validation=validate_password)

            with open('user_secrets.json', 'w+') as f:
                f.write(user_secrets)

            return


        elif key == 98:  # b
            user_secrets = ask_for_user_secrets()
            real_user_secrets = ''
            with open('user_secrets.json', 'r') as f:
                real_user_secrets = f.read()
            with open('output', 'w') as f:
                f.write(user_secrets)
            if decrypt(json.loads(user_secrets)["password"]) != decrypt(json.loads(real_user_secrets)["password"]) and os.path.isfile('user_secrets.json'):
                with open('output', 'w') as f:
                    f.write(user_secrets + '\n' + real_user_secrets)
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

                    stdscr.clear()
                    try:
                        stdscr.addstr('Username or password was incorrect. \
Press ^e to exit the program and try again later.')
                    except Exception:
                        raise Exception('Terminal window is too small')
                    
                    stdscr.refresh()
                    time.sleep(0.01)
            else:
                return

        stdscr.clear()
        try:
            stdscr.addstr(popup_text.display(
                lines_start, lines_stop - 1,
                cols_start, cols_stop))
        except Exception as e:
            raise Exception('Terminal window is too small')
        
        stdscr.refresh()

        time.sleep(0.01)
