#!/bin/bash

# Change directory
cd ../mfc1

# Make a copy from the old file.
cp ./pofiles/de/LC_MESSAGES/mfc1.po \
   ./pofiles/de/LC_MESSAGES/old-mfc1.po

# Create a new .po file with pygettext.
pygettext -o ./pofiles/de/LC_MESSAGES/mfc1.po ./*.py

# Merge the old into the new .po file.
msgmerge -o ./pofiles/de/LC_MESSAGES/mfc1.po \
            ./pofiles/de/LC_MESSAGES/old-mfc1.po \
            ./pofiles/de/LC_MESSAGES/mfc1.po

# Edit the file with poedit.
# Option 'Write the .MO file with saving the .po file.' is activ.
poedit ./pofiles/de/LC_MESSAGES/mfc1.po

echo " "
echo "..Press [enter] when all changes are done."
read TASTE

# move to .mo file
mv -u ./pofiles/de/LC_MESSAGES/mfc1.mo \
      ./locale/de/LC_MESSAGES/mfc1.mo

echo " "
echo "..Press any key to continue."
read TASTE

