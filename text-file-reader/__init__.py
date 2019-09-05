import os
from shutil import copyfile


# add files to bin directory so they can be run from anywhere.

username = os.getcwd().split('/')[2]
bin_dir = f"/Users/{username}/bin"
cwd = os.path.abspath(os.path.dirname(__file__))

# create bin directory if it doesn't already exist
if not os.path.isdir(bin_dir):
    os.mkdir(bin_dir)

# create ascii-art and popup dirs
try:
    os.mkdir(bin_dir + '/ascii-art')
    os.mkdir(bin_dir + '/ascii-art/popups')
except FileExistsError:
    pass

# copy files from cwd to bin
files = ['encrypt.py', 'file-reader.py', 'helpscreen', 'separate_mainloops.py',
         'ascii-art/sign-up.txt', 'ascii-art/popups/donate1.txt',
         'ascii-art/popups/donate2.txt', 'ascii-art/popups/twitter.txt']
cwd_paths = [cwd + '/' + file for file in files]
bin_paths = [bin_dir + '/' + file for file in files]
for cwd_path, bin_path in zip(cwd_paths, bin_paths):
    copyfile(cwd_path, bin_path)
    # print(cwd_path, bin_path)