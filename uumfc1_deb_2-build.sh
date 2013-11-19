#!/bin/bash
WORKDIR=build
VERS="1.0"
cd $WORKDIR/uumfc1-$VERS
debuild
echo " "
echo "..Press [enter] to continue"
read TASTE

