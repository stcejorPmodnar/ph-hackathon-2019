# text-file-reader

Exactly what it sounds like.

*This is not meant for practical use. It began as a hackathon submission, but I missed the deadline, so now I'm finishing it to be happy. The theme of the hackathon was "Overengineered UI", so it's not meant to be easy to use.*

# Installation

## Install with Git

```git clone https://github.com/stcejorPmodnar/ph-hackathon-2019```

## Install with pip

*The better option in my opinion*

```bash
pip install text-file-reader
python -m text-file-reader  # add files to ~/bin
chmod +x ~/bin/text-file-reader  # give permission to main executable
```

# Usage

## Startup

### Installed with git

```python[3] file-reader.py file.txt```

With `file.txt` being the file you want to read.

You can include the flag `-h` if you want to see the helpscreen.

### Installed with pip

Siplmy use the command ```text-file-reader file.txt```

## Interface

Press ^e at any time to quit.

^t - find in file

^b - compile file in your choice of various languages.

Use the arrow keys to move your cursor.
If you attempt to move it off the screen, 
the file contents will scroll accordingly.

You will get an error if your terminal window is too small to display any of the text.

# Contribute

I don't mind pull requests, but I'm done with this project, so don't expect anything.

# OS Compatability and Requirements

**This is only usable on macos**, and I have no plans of making it compatible on windows or linux.

You should have python 3.x installed, but I've yet to test it with anything lower than 3.7.4, 
and I think there are some changes between python 3.6 and 3.7 in multiline string formatting, 
which (as you can imagine) was very important to this project.
