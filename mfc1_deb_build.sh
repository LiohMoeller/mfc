#!/bin/bash
# Delete all *.pyc files.
echo "DELETE all *.pyc files .."
find ./ -name *.pyc -delete

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

# Copy mindfulclock to ./bin
mkdir bin
cp mindfulclock1 ./bin

# Create source tar.gz
tar -czf mfc1-$VERS.tar.gz applications/ bin/ pixmaps/ mfc1/
mv mfc1-$VERS.tar.gz $WORKDIR/

# Delete ./bin and mindfulclock1
rm bin/mindfulclock1
rmdir bin

# Exctract source tar.gz
cd $WORKDIR
mkdir mfc1-$VERS
tar -xzf mfc1-$VERS.tar.gz -C mfc1-$VERS

# dh_make
cd mfc1-$VERS
dh_make -f ../mfc1-$VERS.tar.gz

# Delete not necessary files.
cd debian
rm compat docs *.ex *.Debian *.source source *.EX
rm -r source

# Edit all files in /debian
gedit *

echo " "
echo "..Press [enter] when all changes are done."
read TASTE

# Change directory
cd ..

# Build debian package
debuild

echo " "
echo "..Press [enter] to continue."
read TASTE

