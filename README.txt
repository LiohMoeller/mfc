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
- Go to the directory <dist>
- Get the sourcecode distribution TAR.GZ you like.
  Klick on RAW view, the download will start.


INSTALLATION FROM SOURCECODE DISTRIBUTION
- Unzip the donloaded file. There will be created follewed directorys:
  <./Unity Ubuntu MindfulClock-1>,
  <./Unity Ubuntu MindfulClock-1/alpha>
- Change into the <alpha> directory.
- Follow termical commando (with administrator rights):
  sudo ./setup.py install
  
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
- On a UBUNTU system PYTHON will install follow directorys and files:
    /usr/local/lib/python2.7/dist-packages
        uumfcunitest.py
        uumfcmsg.py
        uumfcdata.py
        uumfcgui.py
        uumfcunitest.pyc
        uumfcmsg.pyc
        uumfcdata.pyc
        uumfcgui.pyc
    /usr/local/
        license.txt
        gpl-3-0_de.html
        gpl-3-0_en.html
    /usr/local/icons
        Icon.253760.png
    /usr/local/icons/16
        go-down.png
        list-add.png -> /usr/local/icons/16
        list-remove.png -> /usr/local/icons/16
        media-playback-start.png -> /usr/local/icons/16
        media-playback-stop.png -> /usr/local/icons/16
        process-stop.png -> /usr/local/icons/16
        system-log-out.png -> /usr/local/icons/16
        system-search.png -> /usr/local/icons/16
        weather-clear.png -> /usr/local/icons/16
    /usr/local/icons/22
        go-down.png
        list-add.png
        list-remove.png
        media-playback-start.png
        media-playback-stop.png
        process-stop.png
        system-log-out.png
        system-search.png
        weather-clear.png
    /usr/local/icons/32
        go-down.png
        list-add.png
        list-remove.png
        media-playback-start.png
        media-playback-stop.png
        process-stop.png
        system-log-out.png
        system-search.png
        weather-clear.png
  - /usr/local/sounds
        Metal_Gong-Dianakc-109711828.wav

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
