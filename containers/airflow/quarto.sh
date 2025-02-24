#!/bin/bash
:'
Script Summary:
- Downloads the Quarto CLI package.
- Extracts it to a local directory.
- Sets up a symbolic link to the Quarto binary in the ~/.local/bin directory.
- Updates the PATH to include this directory.
- Reloads the environment configuration so the quarto command is available immediately.
'

# curl: download quarto from github
# -L : follow redirects in URL
# -o ~/quarto-1.5.43-linux-amd64.tar.gz : where to save output file
curl -L -o ~/quarto-1.5.43-linux-amd64.tar.gz https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.43/quarto-1.5.43-linux-amd64.tar.gz

# create directoty called opt to hold extracted files
# 'opt' = convention for optional add on software thats not part of base system
mkdir ~/opt

# -C ~/opt : extract tarball into opt directory
# -x : extracts files
# -v : verbose, displays files being extracted
# -z : indicates file is gzip compressed
# -f : specifies file to extract

tar -C ~/opt -xvzf ~/quarto-1.5.43-linux-amd64.tar.gz

# create directory in users home directory
# common location for user installed executables on linux
mkdir ~/.local/bin

# creates symbolic link to quarto binary in ~/opt/quarto-1.5.43/bin/quarto
# symbolic link : link that points to another file/folder on a connected file system
# puts link in ~/.local/bin/quarto
# makes quarto accessible from this directory
ln -s ~/opt/quarto-1.5.43/bin/quarto ~/.local/bin/quarto

# add ~/.local/bin to system path 
# adds export PATH=$PATH:~/.local/bin to ~/.profile
# = terminal can run executables in this directory from anywhere, dont need full path
( echo ""; echo 'export PATH=$PATH:~/.local/bin\n' ; echo "" ) >> ~/.profile

# reloads the ~/.profile file which applies the changes to the current shell session
source ~/.profile

# now quarto is available for use! 