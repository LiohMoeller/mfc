#!/bin/bash
# Build source distribution with gztar file.
echo "..Build GZTAR source distribution."
./setup.py sdist --formats=gztar

# Build source distribution wiht zip file
echo "..Build ZIP source distribution."
./setup.py sdist --formats=zip

echo "..Press any key to continue"
read TASTE

