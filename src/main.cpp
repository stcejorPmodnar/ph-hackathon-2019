#include <ncurses.h>
#include <fstream>
#include <string>
#include <iostream>
#include <sstream>
#include <cstring>

using namespace std;

bool replace(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

bool file_exists(const char *fileName) {
    ifstream file(fileName);
    return file.good();
}

int main(int argc, char **argv) {
    /*
    Reads a text file and displays contents to the screen 
    */

   string encoding;

   // Argument handling: 
    for ( int i = 1; i < argc; i++ ) {
        
        string curArg = argv[i];
        
        switch (curArg) {
            case "-h":
                // for ( int x = i + 1; x < i + 6; x++) {
                //     switch (x) {
                //         case i + 1:
                //     }
                // }
                //something should happen here
            break;
            case "-e":
                if ( argv[i++] !== "-l" ){
                    encoding = argv[i++];
                }
            break;
        }
    }

//    if ( argc > 2 ) {
//         cout << "Sorry, only one file can be opened with the free version." << endl;
//         return 1;
//    }
//    else if (argc == 1) {
//         cout << "Specify an input file" << endl;
//         return 1;
//    }
//    else {
//        if (!file_exists(argv[1])) {
//             cout << argv[1] << " is not a file." << endl;
//             return 1;
//         }
//    }

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

    // how far away each coord of the cursor is from its original position
    int add_y;
    int add_x;

    // the text to be displayed to the screen
    string screen_text = file_contents;

    // mainloop
    while (true) {
        int ch = getch();
        clear();

        string cropped_screen_text;
        istringstream screen_text_iss(screen_text);
        int i;
        string line;
        for ( int i = 0; i < COLS && getline(screen_text_iss, line); i++ ) {
            cropped_screen_text.append(line + '\n');
        }

        char * screen_text_char = new char[cropped_screen_text.length() + 1];
        strcpy(screen_text_char, cropped_screen_text.c_str());
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
            
            string last_line;
            istringstream screen_text_iss(screen_text);
            for ( string line; getline(screen_text_iss, line); ) {
                last_line = line;
            }

            string new_last_line;
            for ( int i = 0; i < COLS; i++ ) {
                new_last_line.append(" ");
            }

            replace(screen_text, last_line, new_last_line);
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