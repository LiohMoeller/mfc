Ubuntu Unity MindFulClock One - Uumfc 1

With the Ubuntu Unity MindFulClock you turn your device into a Bell of
Mindfulness. During the day you hear regularly the bell and it gives
you the  opportunity to pause for a moment and enjoy the present of
Mindfulness.


OPERATING SYSTEM
- Uumfc is programmed in Python wiht the GUI- toolkit wxPython. It runs
  on all platforms which support python and wxpython.
- Uumfc is specially designed for Ubuntu with the Unity desktop.


DOWNLOAD FROM GITHUB
- Go to the directory <dist>
- Get the sourcecode distribution, TAR.GZ.
  Klick on RAW view, the download will start.


INSTALLATION FROM THE SOURCECODE DISTRIBUTION
- Make sure that Python 2.7, wxPython 2.8, PyGame 1.9 are installed,
  command line to install:
  <sudo apt-get install python python-wxgtk2.8 python-pygame timidity>
- Extract the donloaded file.
- Go to the directory <../uumfc1/alpha/>
- Run the command line: <sudo ./setup.py install>  
- the program starts with <uumfc1run>


TRUBBLESHOTTING
- Reset all setting: Delete the configuarion, the hidden file <.uumfc1>
  in the home directory.


REMOVE THE SOURCECODE DISTRIBUTION
- On a UBUNTU system delete follow directory and files
  with adminstrator rights:
    </usr/local/lib/python2.7/dist-packages>
    </usr/local/bin/uumfc1run>
    

REMOVE THE SETTINGS
- If the settings are to be removed: Delete the hidden file <.uumfc1>
  in the home directory.


RELEASE NOTES VERSION 1 / alpha
- Cross over Version of MindFulClock.
- Notification with text or sound.
- Specification by user: Time interval in minutes, text notification,
  sound notification.
- Art work and sound theme.
- Sourcecode installation


CONCEPT, DESIGN
  Marcus Möller
  <marcus.moeller@outlook.com>
  <http://apps.microsoft.com/windows/de-de/app/mindfulclock/58063160-9cc6-4dee-9d92-17df4ce4318a>


PROGRAM CODE
  Andreas Ulrich
  <http://erasand.jimdo.com/kontakt/>
  <ulrich3110@gmail.com>


ART WORK
  Marcus Möller (program icon)
  The Tango Project (button icons)


SOUND WORK
  <pv-bell.mp3> by Marcus Möller


15.11.2013 / Andreas Ulrich
