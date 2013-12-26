MindfulClock 1.0

With the MindfulClock you turn your device into a Bell of Mindfulness.
During the day, it will periodically invite the bell and gives you the
opportunity to pause, and enjoy the present moment in mindfulness.


OPERATING SYSTEM
- The MindfulClock is programmed in Python with the GUI toolkit
  wxPython. It runs on all platforms which support Python and
  wxpython.
- It's specially designed for Ubuntu.


RELEASE NOTES 1.0
- Notification with text or sound.
- Specification by user: Time interval in minutes, text notification,
  sound notification, pause function.
- Full clock control in the user interface.
- Taskbar application.
- Ubuntu integration with the Application indicator.
- Artwork and sound theme.
- Debian package.
- Command line options
- Sourcecode installation.
- Internationalisation with pygettext.


DOWNLAD AND INSTALL DEBIAN PACKAGE
- Download the project archive
- Extract the archive to a temporary folder
- Open the <deb> directory
- Run the .deb, the package <mfc1> will be installed.
- You can start the clock with the menu entry, or with the command:
  <mindfulclock1 [OPTIONS]>
    --start-tna         Start the clock minimized in
                        the Taskbar Notification Area.
    --autostart-clock   Start the clock automatically.
    --taskbar           Use the classic taskbar, instead
                        of the application indicator.
    --menu-time         Show the time not beside the
                        taskbar indicator icon.
                        (With --taskbar, this option
                         will be ignored.)
    --help              Show a little help.


USAGE

MindfulClock offers several options. You can define the time interval,
a text message that supports your practise and a bell sound. You can
also disable either the text or the sound notification by clearing the
relevant input box. All changes will be applied on the next startup of
the clock (or by pressing the stop button and the start button again).

The application brings an indicator applet which you will find in the
upper right corner of your Ubuntu Unity desktop. If you are not using
Unity, you could also start the application with the --start-tna 
parameter, which will make use of the traditional systray instead.

From the indicator icon, you can start, stop or pause the clock and
open the main application window.

MindfulClock can by configured to automatically start the clock on
application startup and to start directly to the indicator applet.

The main window can always be minimized to the applet by pressing the
minimize button. Using the exit button will close the application.
 

TROUBBLESHOTTING
- Reset all setting: Delete the configuarion, the hidden file <.mfc1>
  in the home directory.


REMOVE THE DEBIAN PACKAGE
- Remove the package <mfc1> from your system.


REMOVE THE SETTINGS
- If the settings are to be removed: Delete the hidden file <.mfc1>
  in the home directory.


DOWNLOAD SOURCECODE DISTRIBUTION FROM GITHUB
- Download the project archive
- Extract the archive to a temporary folder
- Open the <dist> directory

INSTALLATION THE SOURCECODE DISTRIBUTION
- Make sure that Python 2.7, wxPython 2.8, PyGame 1.9 are installed.
  The technical packages timidity & python-appindicator may help.
  Command line to install:
  <sudo apt-get install python python-wxgtk2.8 python-pygame>
  <sudo apt-get install timidity python-appindicator>
- Extract the donloaded file.
- Go to the directory <mfc1-1.0>, where the file <setup.py> is placed.
- Run the command line: <sudo ./setup.py install>
- Python installs the source distribution.
- the program starts with the command:
  <mindfulclock1 [OPTIONS]>
    --start-tna         Start the clock minimized in
                        the Taskbar Notification Area.
    --autostart-clock   Start the clock automatically.
    --taskbar           Use the classic taskbar, instead
                        of the application indicator.
    --menu-time         Show the time not beside the
                        taskbar indicator icon.
                        (With --taskbar, this option
                         will be ignored.)
    --help              Show a little help.
- For a program starter icons are placed in </mfc1/icons> in the
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


DOCUMENTATION
- start the file /doxygen-docu/html/index.html of this repository.


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
- Marcus Möller
  <marcus.moeller[AT]ubuntu[DOT]com>


PROGRAM CODE
- Andreas Ulrich
  <http://erasand.jimdo.com/kontakt/>
  <ulrich3110[AT]gmail[DOT]com>


ARTWORK
- Marcus Möller (program icon)
  The Tango Project (button icons)


SOUND 
- <pv-bell.ogg> by Marcus Möller and the WakeUp community


26.12.2013 / Andreas Ulrich, Marcus Möller
