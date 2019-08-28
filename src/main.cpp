#include <ncurses.h>
#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

using namespace std;

bool file_exists(const char *fileName) {
    ifstream file(fileName);
    return file.good();
}

int main(int argc, char **argv) {
    /*
    Reads a text file and displays contents to the screen 
    */

   // Argument handling: 
   if ( argc > 2 ) {
        cout << "Sorry, only one file can be opened with the free version." << endl;
        return 1;
   }
   else if (argc == 1) {
        cout << "Specify an input file" << endl;
        return 1;
   }
   else {
       if (!file_exists(argv[1])) {
            cout << argv[1] << " is not a file." << endl;
            return 1;
        }
   }

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

    // setup screen and input
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    scrollok(stdscr, TRUE);

    // how far away each coord of the cursor is from its original position
    int add_y;
    int add_x;

    // the text to be displayed to the screen
    string screen_text = file_contents;

    // mainloop
    while (true) {
        int ch = getch();
        clear();
        char * screen_text_char = new char[screen_text.length() + 1];
        strcpy(screen_text_char, screen_text.c_str());
        printw(screen_text_char);
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
        } else if (ch == 20) /* ^t (find in file) */ {
            // change bottom line of screen text to blank line
            
            int newline_count = 0;
            
        }
        
        // wmove cursor only if x and y will be inside of window bounds;
       
       
        int x;
        int y;
        getyx(stdscr, x, y);
        if ((0 <= x + add_x <= COLS) && (0 <= y + add_y <= LINES)) {
            wmove(stdscr, y + add_y, x + add_x);
        }
    }
    return 0;
}