Ubuntu Unity MindFulClock 1.0.1

With the Ubuntu Unity MindFulClock you turn your device into a Bell of
Mindfulness. During the day you hear regularly the bell and it gives
you the  opportunity to pause for a moment and enjoy the present of
Mindfulness.


OPERATING SYSTEM
- Uumfc is programmed in Python wiht the GUI- toolkit wxPython. It runs
  on all platforms which support python and wxpython.
- Uumfc is specially designed for Ubuntu with the Unity desktop.


DOWNLOAD SOURCECODE DISTRIBUTION FROM GITHUB
- Go to the directory <dist>
- Get the sourcecode distribution, TAR.GZ.
  Klick on RAW view, the download will start.


INSTALLATION FROM THE SOURCECODE DISTRIBUTION
- Make sure that Python 2.7, wxPython 2.8, PyGame 1.9 are installed,
  command line to install:
  <sudo apt-get install python python-wxgtk2.8 python-pygame timidity>
- Extract the donloaded file.
- Go to the directory <uumfc1>, where the file <setup.py> is placed.
- Run the command line: <sudo ./setup.py install>
- the program starts with <uumfc1run>


DOWNLAD AND INSTALL DEBIAN PACKAGE
- Go to the directory <deb>
- Get the .deb package.
  Klick on RAW view, the download will start.
- Run the .deb, the package <uumfc1> will be installed.


TRUBBLESHOTTING
- Reset all setting: Delete the configuarion, the hidden file <.uumfc1>
  in the home directory.


REMOVE THE SOURCECODE DISTRIBUTION
- On a UBUNTU system delete follow directory and files
  with adminstrator rights:
    </usr/local/lib/python2.7/dist-packages>
    </usr/local/bin/uumfc1run>
    

REMOVE THE DEBIAN PACKAGE
- Remove the package <uumfc1> from your system.
    

REMOVE THE SETTINGS
- If the settings are to be removed: Delete the hidden file <.uumfc1>
  in the home directory.


RELEASE NOTES 1.0.1
- Cross over Version of MindFulClock.
- Notification with text or sound.
- Specification by user: Time interval in minutes, text notification,
  sound notification.
- Art work and sound theme.
- Sourcecode installation
- Debian package
- Internationalisation with pygettext.


GERMAN TRANSLATIONS
- PO files uumfc1/pofiles/de/LC_MESSAGES/uumfc1.po
- MO files locale/de/LC_MESSAGES/uumfc1.mo
- The work directory for follwing command is:
  </uumfc1>
- Make a copy from the old file:
  <cp ./pofiles/de/LC_MESSAGES/uumfc1.po \
   ./pofiles/de/LC_MESSAGES/old-uumfc1.po>
- Create a new .po file with pygettext:
  <pygettext -o ./pofiles/de/LC_MESSAGES/uumfc1.po ./*.py>
- Merge the old into the new .po file:
  <msgmerge -o ./pofiles/de/LC_MESSAGES/uumfc1.po \
   ./pofiles/de/LC_MESSAGES/old-uumfc1.po \
   ./pofiles/de/LC_MESSAGES/uumfc1.po>
- Make the translation, edit the .po file:
  - Replace <line Content-Type: text/plain; charset=CHARSET> with 
    <line Content-Type: text/plain; charset=utf-8>.
  - By editing the .PO file with the PO-Edit, you can optionally write
    the .MO file with saving the .po file.
    After this, yo just has to move the .mo file:
    <mv -u ./pofiles/de/LC_MESSAGES/uumfc1.mo \
     ./locale/de/LC_MESSAGES/uumfc1.mo>
  - Create the .mo file manually:
    <msgfmt --output-file ./locale/de/LC_MESSAGES/uumfc1.mo \
     ./pofiles/de/LC_MESSAGES/uumfc1.po>


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


17.11.2013 / Andreas Ulrich
