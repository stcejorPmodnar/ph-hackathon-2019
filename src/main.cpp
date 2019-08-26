#include <ncurses.h>

using namespace std;

int main() {
    
    // setup screen and input
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    scrollok(stdscr, TRUE);
    
    // mainloop
    while (true) {
        clear();
        printw("hello world");
        refresh();
        int ch = getchar();
        if (ch == 113) {
            endwin();
            break;
        }
    }
    return 0;
}