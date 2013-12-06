#!/bin/bash

# change directory
cd ..

# Delete all *.pyc files.
echo "DELETE all *.pyc files .."
find ./ -name *.pyc -delete

# Build source distribution with gztar file.
echo "..Build GZTAR source distribution."
./setup.py sdist --formats=gztar

# Build source distribution with zip file
# echo "..Build ZIP source distribution."
# ./setup.py sdist --formats=zip

echo "..Press any key to continue"
read TASTE

