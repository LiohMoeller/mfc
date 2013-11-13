Ubuntu Unity MindFulClock - Uumfc

With the Ubuntu Unity MindfulClock you turn your device into a Bell of
Mindfulness. During the day you hear regularly the bell and it gives
you the  opportunity to pause for a moment and enjoy the present of
Mindfulness.


OPERATING SYSTEM
- Uumfc is programmed in Python wiht the GUI- toolkit wxPython. It runs
  on all platforms which support python and wxpython.
- Uumfc is specially designed for Ubuntu with the Unity desktop.


DOWNLOAD FROM GITHUB
- Download the repository with the <Download ZIP> button.


INSTALLATION FROM SOURCECODE DISTRIBUTION
- Unzip the ZIP file into the desired program directory,
  for example  <~/Downloads/uumfc-master>.
- Change into this directory.
- Build 1st a sourcecode distribution, command line for the terminal:
  python setup.py sdist
  rm 'Unity Ubuntu MindfulClock-1'
- Install the sourcecode distribution, command line for the terminal:
  
- 
- Requirements: Python 2.7, wxPython 2.8, PyGame 1.9.
  Command line for the terminal:
    sudo apt-get install python python-wxgtk2.8 python-pygame

- Create a starter for the python module uumfcgui.py,
  for example  <~/uumfc/modules/uumfcgui.py>.
- The start module must running in the directory of uumfcgui.py,
  for example  <~/uumfc/modules>.


KNOWN PROBLEMS
- By the error message "there is no soundcard" install the package
  "timidity".
  Command line for the terminal:  sudo apt-get install timidity


TRUBBLESHOTTING
- Reset all setting: Delete the configuarion, the hidden file <.uumfc>
  in the home directory.


MANUAL REMOVAL
- Delete the program directory,
  for example  <~/uumfc>.
- If the settings are to be removed: Delete the hidden file <.uumfc> in
  the home directory.


RELEASE NOTES VERSION 0 / beta
- Cross over Version of MindFlucClock.
- Notification with text or sound.
- Specification by user: Time interval in minutes, text notification,
  sound notification.


CONCEPT, DESIGN
  Marcus Möller
  <marcus.moeller@outlook.com>
  <http://apps.microsoft.com/windows/de-de/app/mindfulclock/58063160-9cc6-4dee-9d92-17df4ce4318a>


PROGRAM CODE
  Andreas Ulrich
  <http://erasand.jimdo.com/kontakt/>
  <ulrich3110@gmail.com>


ART WORK
  Marcus Möller (Program icon)
  The Tango Project (Button icons)


SOUND WORK
  <http://soundbible.com/2062-Metal-Gong-1.html>
  <Metal_Gong-Dianakc-109711828.wav>
  License Attribution 3.0


12.11.2013 / Andreas Ulrich
