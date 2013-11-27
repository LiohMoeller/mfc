MindfulClock 1.0

With the MindfulClock you turn your device into a Bell of Mindfulness.
During the day, it will periodically invite the bell and gives you the
opportunity to pause, and enjoy the present moment in mindfulness.

OPERATING SYSTEM
- The MindfulClock is programmed in Python wiht the GUI toolkit
  wxPython. It runs on all platforms which support python and wxpython.
- Its specially designed for Ubuntu with the Unity desktop.


DOWNLAD AND INSTALL DEBIAN PACKAGE
- Go to the directory <deb>
- Get the .deb package.
  Klick on RAW view, the download will start.
- Run the .deb, the package <mfc1> will be installed.
- You can start the clock with the menu entry, or with the command:
  <mfc1deb [OPTIONS]>
    --start-minim   Start the clock minimized.
    --tb-icon       Use the classic system tray, instead
                    of the application indicator.
    --help          Show a little help.


TRUBBLESHOTTING
- Reset all setting: Delete the configuarion, the hidden file <.mfc1>
  in the home directory.


REMOVE THE DEBIAN PACKAGE
- Remove the package <mfc1> from your system.


REMOVE THE SETTINGS
- If the settings are to be removed: Delete the hidden file <.mfc1>
  in the home directory.


DOWNLOAD SOURCECODE DISTRIBUTION FROM GITHUB
- Go to the directory <dist>
- Get the .tar.gz file.
  Klick on RAW view, the download will start.


INSTALLATION THE SOURCECODE DISTRIBUTION
- Make sure that Python 2.7, wxPython 2.8, PyGame 1.9 are installed.
  The technical packages timidity & python-appindicator may help.
  Command line to install:
  <sudo apt-get install python python-wxgtk2.8 python-pygame>
  <sudo apt-get install timidity python-appindicator>
- Extract the donloaded file.
- Go to the directory <mfc1-1.0>, where the file <setup.py> is placed.
- Run the command line: <sudo ./setup.py install>
- the program starts with the command:
  <mfc1dist [OPTIONS]>
    --start-minim   Start the clock minimized.
    --tb-icon       Use the classic system tray, instead
                    of the application indicator.
    --help          Show a little help.
- For a program starter icons are placed in </pixmaps> in the
  repisotory.
- If application indicator icon is not displayed, please copy the file
  </pixmaps/alarm-clock-indicator.png> from the repository to
  </usr/share/pixmaps>.


REMOVE THE SOURCECODE DISTRIBUTION
- On a UBUNTU system delete follow directory and files
  with adminstrator rights:
  directory </usr/local/lib/python2.7/dist-packages/mfc1>
  file </usr/local/lib/python2.7/dist-packages/mfc1-1.0.egg-info>
  file </usr/local/bin/mfc1dist>


RELEASE NOTES 1.0
- Notification with text or sound.
- Specification by user: Time interval in minutes, text notification,
  sound notification.
- Art work and sound theme.
- Sourcecode installation.
- Debian package.
- Internationalisation with pygettext.
- System-tray application.
- Ubuntu Unity integration wiht the Application indicator.
- Command line options


GERMAN TRANSLATIONS
- PO files mfc1/pofiles/de/LC_MESSAGES/mfc1.po
- MO files mfc1/locale/de/LC_MESSAGES/mfc1.mo
- The work directory for follwing command is:
  </mfc1>
- Make a copy from the old file:
  <cp ./pofiles/de/LC_MESSAGES/mfc1.po \
   ./pofiles/de/LC_MESSAGES/old-mfc1.po>
- Create a new .po file with pygettext:
  <pygettext -o ./pofiles/de/LC_MESSAGES/mfc1.po ./*.py>
- Merge the old into the new .po file:
  <msgmerge -o ./pofiles/de/LC_MESSAGES/mfc1.po \
   ./pofiles/de/LC_MESSAGES/old-mfc1.po \
   ./pofiles/de/LC_MESSAGES/mfc1.po>
- Make the translation, edit the .po file:
  - Replace <line Content-Type: text/plain; charset=CHARSET> with
    <line Content-Type: text/plain; charset=utf-8>.
  - By editing the .PO file with the PO-Edit, you can optionally write
    the .MO file with saving the .po file.
    After this, yo just has to move the .mo file:
    <mv -u ./pofiles/de/LC_MESSAGES/mfc1.mo \
     ./locale/de/LC_MESSAGES/mfc1.mo>
  - Create the .mo file manually:
    <msgfmt --output-file ./locale/de/LC_MESSAGES/mfc1.mo \
     ./pofiles/de/LC_MESSAGES/mfc1.po>


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


26.11.2013 / Andreas Ulrich
