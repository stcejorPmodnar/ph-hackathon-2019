import time
import sys
import subprocess
import os.path
import string
import json

from encrypt import encrypt, decrypt


USER_SECRETS = '{"username": "%s","password": "%s"}'


class Continue(Exception):
    """Dummy exception for raising to exit outermost function"""


class FileText:
    """An object to represent the text being displayed on the screen"""

    def __init__(self, lines, cols, real_text):
        # access current char in grid by grid[x][y]
        self.grid = [[' ' for _ in range(lines)] for _ in range(cols)]
        self.real_text = real_text

    def replace(self, x, y, char):
        """replaces one char in the canvas at location (x, y)"""
        self.grid[x][y] = char

    def display(self, lines_start, lines_stop, cols_start, cols_stop):
        """Displays a certain section of the text"""
        transposed = [[col[i] for col in self.grid[cols_start:cols_stop]]
                      for i in list(range(len(self.grid[0])))[lines_start:lines_stop]]
        return '\n'.join([''.join(line) for line in transposed])


class InputLine:
    def __init__(self, length):
        self.chars = [' ' for _ in range(length)]
    
    def replace(self, index, char):
        self.chars[index] = char
    
    @property
    def display(self):
        return ''.join(self.chars)


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


def popup(stdscr, filename, lines, cols):
    """Displays popup until q is pressed"""

    path = os.path.abspath(filename)
    with open(path, 'r') as f:
        ascii_art = f.read()

    ascii_art_lines = ascii_art.split('\n')

    ascii_file_text = FileText(
        len(ascii_art_lines),
        max([len(i) for i in ascii_art_lines]),
        ascii_art)

    for y, line in enumerate(ascii_art_lines):
        for x, char in enumerate(line):
            ascii_file_text.replace(x, y, char)

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

        elif key == 113:  # q (exit popup)
            return

        stdscr.clear()
        try:
            stdscr.addstr(ascii_file_text.display(0, lines, 0, cols - 1))
        except Exception:
            raise Exception('Terminal window is too small')

        stdscr.refresh()
        time.sleep(0.01)


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


def compile_screen(stdscr, filename, lines, cols):
    """Screen that provides options for compiling code in file"""

    def compile_in_language(extension, compiler):
        """Interface to compile the file in any language."""

        error = False

        def compile_file(compiling_command):
            """Actually compile the file into an executable"""

            # check if compiler exists
            try:
                try:
                    subprocess.check_output([compiling_command])
                except subprocess.CalledProcessError:
                    pass
            except FileNotFoundError:
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
                    
                    elif key == 113:  # "q"
                        raise Continue

                    stdscr.clear()
                    try:
                        stdscr.addstr("No such compiler. Press 'q' to continue to viewing file.")
                    except Exception:
                        raise Exception('Terminal window is too small')
                    stdscr.refresh()

                    time.sleep(0.01)

            if filename.split('.')[-1] != extension:
                # file has incorrect extension

                # copy file contents into new file with correct extension
                with open(filename, 'r') as f:
                    contents = f.read()

                new_filename = filename.split('.')[0] + f'.{extension}'

                with open(new_filename, 'w+') as f:
                    f.write(contents)

                # compile file using compiler
                try:
                    compile_output = subprocess.check_output([compiler, new_filename]).decode('utf-8')
                    error = False
                except subprocess.CalledProcessError as e:
                    compile_output = e.returncode
                    error = True
            else:
                try:
                    compile_output = subprocess.check_output([compiler, filename]).decode('utf-8')
                    error = False
                except subprocess.CalledProcessError as e:
                    compile_output = e.returncode
                    error = True
            
            if error:
                display = f"Code compilation was unsuccessful. Command returned the following erros:\n{compile_output}.\n\
Press 'q' to continue."
            else:
                if compile_output == "":
                    display = "Code successfully compiled with zero errors.\nPress 'q' to continue."
                else:
                    display = f"Code compiled with following output:\n{compile_output}.\nPress 'q' to continue."

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
                
                elif key == 113:  # q
                    raise Continue

                stdscr.clear()
                try:
                    stdscr.addstr(display)
                except Exception:
                    raise Exception('Terminal window is too small')

                stdscr.refresh()

                time.sleep(0.01)

        try:
            subprocess.check_output(['which', compiler]).decode('utf-8')
            compile_file(compiler)
        except subprocess.CalledProcessError as e:
            # user doesn't have compiler

            DONT_HAVE_COMPILER_TEXT = \
f"""You don't seem to have {compiler} installed.
Would you like to:
not compile at all [a]\tuse a different compiler [b]"""

            def ask_for_compiler():

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
                        raise Continue()

                    elif key == 98:  # b
                        line = InputLine(cols - 1)
                        for i, char in enumerate('COMPILER:'):
                            line.replace(i, char)
                        current_space = len('COMPILER:') + 1
                        new_compiler = ''

                        while True:
                            key = stdscr.getch()

                            current_space = default_prompt_mainloop(
                                stdscr, key, lines, cols, line, current_space, 'COMPILER:')

                            if key == 5: # ^e (quit)
                                ask_last = True
                                for i in range(10):
                                    if not ask_to_quit(stdscr, lines, cols, i, False):
                                        ask_last = False
                                        break
                                if ask_last:
                                    ask_to_quit(stdscr, lines, cols, 10, True)
                            
                            elif key == 10: # enter
                                new_compiler = ''.join(line.chars[len('COMPILER:') + 1:current_space])
                                return new_compiler

                            total_display = DONT_HAVE_COMPILER_TEXT + '\n' + line.display
                            stdscr.clear()
                            try:
                                stdscr.addstr(total_display)
                            except Exception:
                                raise Exception('Terminal window is too small')

                            stdscr.refresh()

                            time.sleep(0.01)
                    
                    stdscr.clear()
                    try:
                        stdscr.addstr(DONT_HAVE_COMPILER_TEXT)
                    except Exception:
                        raise Exception('Terminal window is too small')
                    stdscr.refresh()

                    time.sleep(0.01)

            new_compiler = ask_for_compiler()

            compile_file(new_compiler)

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

        elif key == 99:  # "c" (to compile in c)
            try:
                compile_in_language('c', 'gcc')
            except Continue:
                return

        elif key == 112:  # "p" (to compile in c++)
            try:
                compile_in_language('cpp', 'g++')
            except Continue:
                return

        elif key == 106:  # "j" (to compile in java)
            try:
                compile_in_language('java', 'javac')
            except Continue:
                return

        elif key == 114:  # "r" (to compile in rust)
            try:
                compile_in_language('rs', 'rustc')
            except Continue:
                return

        elif key == 115:  # "s" (to compile in c#)
            try:
                compile_in_language('cs', 'mcs')
            except Continue:
                return

        stdscr.clear()
        try:
            stdscr.addstr(
"""Choose language to compile file in.
C [c]\tC++ [p]\tJava [j]\tRust [r]\tc# [s]""")
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

        current_space = default_prompt_mainloop(
            stdscr, key, lines, cols, line, current_space, 'FIND IN FILE:')

        if key == 5: # ^e (quit)
            ask_last = True
            for i in range(10):
                if not ask_to_quit(stdscr, lines, cols, i, False):
                    ask_last = False
                    break
            if ask_last:
                ask_to_quit(stdscr, lines, cols, 10, True)

        elif key == 24: # ^x
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

        if len(file_text.grid[0]) > lines - 1:
            stdscr.move(lines - 1, current_space)
        else:
            stdscr.move(len(file_text.grid[0]), current_space)

        stdscr.refresh()

        time.sleep(0.01)

    # search for all groups of words in lines
    # (credit goes to my mom for coming up with this idea for the ui overengineering)
    pattern_lines = {}
    words = pattern.split(' ')
    combinations = []
    for n in range(1, len(words) + 1):
        groups = [[words[i:i + n] for i in range(x, len(words), n)] for x in range(n)]
        for group in groups:
            for g in group:
                if len(g) == n:
                    combinations.append(' '.join(g))
    
    for combination in combinations:
        for ln, l in enumerate(file_text.real_text.split('\n')):
            if combination in l:
                if combination in list(pattern_lines.keys()):
                    pattern_lines[combination].append(f'{l} ({ln})')
                else:
                    pattern_lines[combination] = [f'{l} ({ln})']

    if pattern_lines != {}:  # there were lines containing at least one word in the search
        string_groups = []
        for combination in pattern_lines.keys():
            group_lines = [f'Lines containing {combination}:', ''] + pattern_lines[combination] + ['']
            string_groups.append('\n'.join(group_lines))
        string = '\n'.join(string_groups)
        string_lines = string.split('\n')
        found_text_cols = max([len(i) for i in string_lines])
        found_text_lines = len(string_lines)
        found_text = FileText(found_text_lines, found_text_cols, string)

        for y, l in enumerate(string_lines):
            for x, char in enumerate(l):
                found_text.replace(x, y, char)
    else:   # no lines contained any of the words in the search
        string = "No instances of this text were found in file"
        found_text = FileText(1, len(string), string)
        for i, char in enumerate(string):
            found_text.replace(i, 0, char)
    
    add_x = 0
    add_y = 0

    while True:
        key = stdscr.getch()

        x_changed = False
        y_changed = False

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
            stdscr.addstr(found_text.display(lines_start, lines_stop, cols_start, cols_stop))
        except Exception:
            raise Exception('Terminal window is too small')

        # move cursor
        move = True
        y, x = stdscr.getyx()
        new_x = x + add_x
        new_y = y + add_y
        if x_changed:
            if new_x >= cols:
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
            if new_y > lines - 1:
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
            if (
                    (decrypt(json.loads(user_secrets)["password"]) !=
                     decrypt(json.loads(real_user_secrets)["password"])
               ) and
                    os.path.isfile('user_secrets.json')):
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
