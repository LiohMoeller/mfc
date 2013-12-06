#!/bin/bash

# Build docu
doxygen mfc-dox

echo " "
echo "..Press [enter] to show documentation."
read TASTE

# Show html
firefox ../doxygen-docu/html/index.html

