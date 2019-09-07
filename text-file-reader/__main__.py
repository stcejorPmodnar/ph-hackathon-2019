import os
from shutil import copyfile

# add files to bin directory so they can be run from anywhere.

username = os.getcwd().split('/')[2]
bin_dir = f"/Users/{username}/bin"
cwd = os.path.abspath(os.path.dirname(__file__))

# create necessary dirs

def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

mkdir(bin_dir)
mkdir(bin_dir + '/ascii-art')
mkdir(bin_dir + '/ascii-art/popups')

# copy files from cwd to bin
files = ['encrypt.py', 'helpscreen', 'separate_mainloops.py',
        'ascii-art/sign-up.txt', 'ascii-art/popups/donate1.txt',
        'ascii-art/popups/donate2.txt', 'ascii-art/popups/twitter.txt',
        'file-reader.py']
cwd_paths = [cwd + '/' + file for file in files]
bin_paths = [bin_dir + '/' + file for file in files]
for cwd_path, bin_path in zip(cwd_paths, bin_paths):
    copyfile(cwd_path, bin_path)

with open(f'{bin_dir}/text-file-reader', 'w+') as f:
    f.write('#!/bin/bash\npython3 ~/bin/file-reader.py $@')