#include <ncurses.h>
#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

using namespace std;

int main(int argc, char **argv) {
    /*
    Reads a text file and displays contents to the screen 
    */

    string line;
    ifstream file (argv[1]);

    string file_contents;

    if (file.is_open()) {
        while (getline(file, line)) {
            string a;
            if (file_contents == a) {
                file_contents.append(line);
            } else {
                file_contents.append('\n' + line);
            }
        }
    }

    // convert file_contents to char array
    char * file_contents_char_arr = new char[file_contents.length() + 1];
    strcpy(file_contents_char_arr, file_contents.c_str());

    // setup screen and input
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    scrollok(stdscr, TRUE);

    // how far away each coord of the cursor is from its original position
    int add_y;
    int add_x;

    // mainloop
    while (true) {
        int ch = getch();
        clear();
        printw(file_contents_char_arr);
        refresh();
        if (ch == 113) /* "q" */{
            endwin();
            break;
        } else if (ch == 258) /* down arrow but scroll up */ {
            add_y -= 1;
        } else if (ch == 259) /* up arrow but scroll down */ {
            add_y += 1;
        } else if (ch == 261) /* right arrow but scroll left */ {
            add_x -= 1;
        } else if (ch == 260) /* left arrow but scroll right */ {
            add_x += 1;
        }
        int x;
        int y;
        getyx(stdscr, x, y);
        wmove(stdscr, y + add_y, x + add_x);
    }
    return 0;
}