#!/bin/bash
# delete directory /usr/local/lib/python2.7/dist-packages/mfc1
echo " "
echo "Delete directory /usr/local/lib/python2.7/dist-packages/mfc1"
echo "with files?  Press [enter] to continue, [ctrl]-[c] to cancel."
read Taste
sudo rm -r /usr/local/lib/python2.7/dist-packages/mfc1

# delete file /usr/local/lib/python2.7/dist-packages/mfc1-*.egg-info
echo " "
echo "Delete file /usr/local/lib/python2.7/dist-packages/"
echo "                                     mfc1-*.egg-info ?"
echo "Press [enter] to continue, [ctrl]-[c] to cancel."
read Taste
sudo rm /usr/local/lib/python2.7/dist-packages/mfc1-*.egg-info

# delete file /usr/local/bin/mfc1dist
echo " "
echo "Delete file /usr/local/bin/mfc1dist?"
echo "Press [enter] to continue, [ctrl]-[c] to cancel."
read Taste
sudo rm /usr/local/bin/mfc1dist

echo "..Press any key to continue"
read TASTE

