#!/bin/bash
# Prepare.
DEBEMAIL="ulrich3110@gmail.com"
DEBFULLNAME="Andreas Ulrich"
WORKDIR=build
VERS="1.0"
# Debian variables.
export DEBEMAIL
export DEBFULLNAME
# Create working directory.
mkdir $WORKDIR
# Create source tar.gz
tar -czf uumfc1-$VERS.tar.gz applications/ bin/ pixmaps/ uumfc1/
mv uumfc1-$VERS.tar.gz $WORKDIR/
# Exctract source tar.gz
cd $WORKDIR
mkdir uumfc1-$VERS
tar -xzf uumfc1-$VERS.tar.gz -C uumfc1-$VERS
# dh_make
cd uumfc1-$VERS
dh_make -f ../uumfc1-$VERS.tar.gz
# Delete not necessary files.
cd debian
rm compat docs *.ex *.Debian *.source source *.EX
rm -r source
# Show directory
echo " "
ls
echo " "
echo "Please edit those files .."
echo "..Press [enter] to continue"
read TASTE

