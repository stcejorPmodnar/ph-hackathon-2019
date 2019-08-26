#include <ncurses.h>
#include <fstream>
#include <string>
#include <iostream>

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

    // mainloop
    while (true) {
        clear();
        printw(file_contents_char_arr);
        refresh();
        int ch = getchar();
        if (ch == 113) /* "q" */ {
            endwin();
            break;
        }
    }
    return 0;
}