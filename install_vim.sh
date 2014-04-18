#!/bin/bash

# This script install vim with X and python support using the PKGBUILD from ABS

# Get latest vim from ABS
sudo abs extra/vim

# Create temp directory
tempdir=$(/bin/mktemp -d)

# Make a local copy of vim within the temp directory
cp -r /var/abs/extra/vim ${tempdir}

# Go to tempdir/vim
cd ${tempdir}/vim

# Replace "--with-x=no" with "--with-x=yes" in PKGBUILD
sed -i "s/--with-x=no/--with-x=yes/g" PKGBUILD
# Replace "--disable-python" with "--enable-python" in KPGBUILD
sed -i "s/--disable-python/--enable-python/g" PKGBUILD

# Build the package
makepkg

# Get files to install
VIM_RUNTIME=$(ls | egrep "^vim-runtime-[0-9\.\-]+-x86_64\.pkg\.tar\.xz$")
VIM=$(ls | egrep "^vim-[0-9\.\-]+-x86_64\.pkg\.tar\.xz$")

# Install vim and vim-runtime
sudo pacman -U ${VIM_RUNTIME} ${VIM}

