# text-file-reader

Exactly what it sounds like.
*This is not meant for practical use. It began as a hackathon submission, but I missed the deadline, so now I'm finishing it to be happy. The theme of the hackathon was "Overengineered UI", so it's not meant to be easy to use.*

# Installation

## Install with Git

```git clone https://github.com/stcejorPmodnar/ph-hackathon-2019```

## Install with pip

*Coming soon*

# Usage

## Startup

As of right now, it's just

```python[3] file-reader.py file.txt```

With `file.txt` being the file you want to read.

You can include the flag `-h` if you want to see the helpscreen.

## Interface

Press ^e at any time to quit.

^t - find in file

^b - compile file in your choice of various languages.

Use the arrow keys to move your cursor.
If you attempt to move it off the screen, 
the file contents will scroll accordingly.

You will get an error if your terminal window is too small to display any of the text.

# Contribute

Though I wouldn't mind any pull requests, wait for the first stable release to contribute.

# Requirements

Because of the compile option, this likely won't work on windows, 
so I won't even bother to add stuff about installing windows-curses to the setup.py.

It should in theory work on linux or any of its distros, 
but I doubt it since I have little experience with the OS, and I haven't done any testing with it.

You should have python 3.x installed, but I've yet to test it with anything lower than 3.7.4, 
and I think there are some changed between python 3.6 and 3.7 in multiline string formatting, 
which (as you can imagine) was very important to this project.