#!/usr/bin/python
# -*- coding: utf-8 -*-

# With the MindfulClock you turn your device into a Bell of Mindfulness.
# Concept, Design: Marcurs Möller
#                  <marcus.moeller@outlook.com>
#                  <http://apps.microsoft.com/windows/de-de/app/
#                   mindfulclock/58063160-9cc6-4dee-9d92-17df4ce4318a>
# Programming: Andreas Ulrich
#              <ulrich3110@gmail.com>,
#              <http://erasand.jimdo.com/kontakt/>
#
# This file is part of the "MindfulClock".
# "MindfulClock" is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# "MindfulClock" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details. You should
# have received a copy of the GNU General Public License along with
# "MindfulClock".  If not, see <http://www.gnu.org/licenses/>.


import os
import time
import wx
import pygame
from data import Data
from lock import Lock
from popup import Popup
from taskbaricon import TBIcon
from unity import AppIndicator


# name for translations texts
_ = wx.GetTranslation


class GUI(wx.Frame):
    '''mfc1.GUI(tna, clock, menu, tbicon)

    GUI of the MindfulClock.
    tna = True, False, start in the taskbar notification area.
    clock = True, False, start clock automatically.
    menu = True, False, show the time not beside te indicator.
    tbicon = True, False, use instead of appindicator wx.TaskBarIcon.

    '''

    def __init__(self, tna, clock, menu, tbicon):
        # Data object.
        self.__data = Data()
        # Package directory
        self.__dir = self.determine_path()
        # Internationalisation
        self.set_in18()
        # Load saved datas.
        self.config_load()
        # Get frame title, frame size and icon.
        title = self.__data.get_sys('frame_title')
        size = self.__data.get_user('frame_size')
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_name'))
        # Subclass
        wx.Frame.__init__(self,
                          parent=None,
                          id=wx.ID_ANY,
                          title=title,
                          size=size)
        # Lock file
        userid = wx.GetUserId()
        wxpath = wx.StandardPaths.Get()
        userdir = wxpath.GetDocumentsDir()
        self.__lock = Lock(path=userdir, userid=userid)
        self.__lockwrite = False
        if self.__lock.is_lock():
            # Lock file exist.
            if self.start_question():
                # Start the clock.
                self.__lock.write_lock()
                self.__lockwrite = True
            else:
                # Exit the program.
                self.Close()
        else:
            # Lock file don't exist.
            self.__lock.write_lock()
            self.__lockwrite = True
        # Icon
        if icon.endswith('.png'):
            self.SetIcon(wx.Icon(name=icon, type=wx.BITMAP_TYPE_PNG))
        # GUI border style and distance between widgets.
        bstyl = self.__data.get_sys('gui_borderstyle')
        guiborders = {'simple': wx.SIMPLE_BORDER,
                      'raised': wx.RAISED_BORDER,
                      'sunken': wx.SUNKEN_BORDER,
                      'no': wx.NO_BORDER}
        if bstyl in guiborders:
            self.__bstyl = guiborders[bstyl]
        else:
            self.__bstyl = wx.SIMPLE_BORDER
        self.__bdist = self.__data.get_sys('gui_borderdist')
        if not self.__bdist:
            self.__bdist = 5
        # Set attributes for time interval and sound file.
        self.__interval = self.__data.get_user('interval')
        self.__sound = os.path.join(self.__dir,
                                    self.__data.get_user('sound'))
        # time interval.
        intervalbox = self.init_interval()
        # Text notification.
        textbox = self.init_text()
        # Sound notification.
        soundbox = self.init_sound()
        # Clock control.
        controlbox = self.init_buttons()
        # Timer
        self.__timer = wx.Timer(self, 1)
        self.Bind(event=wx.EVT_TIMER,
                  handler=self.on_timer,
                  source=self.__timer)
        # Clock status
        self.__clockstatus = False
        # Exit bindings.
        self.Bind(event=wx.EVT_CLOSE, handler=self.on_system_close)
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=intervalbox,
                 proportion=0,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vbox.Add(item=textbox,
                 proportion=1,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vbox.Add(item=soundbox,
                 proportion=0,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vbox.Add(item=controlbox,
                 proportion=0,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        self.SetSizer(vbox)
        # Disable stop & pause button
        self.__btnstop.Enable(False)
        self.__btnpause.Enable(False)
        # Clock not paused.
        self.__pausetime = -99
        # System tray from command line options
        if tna:
            # Start in the taskbar.
            self.__tna = True
        else:
            if self.__miniopt.GetValue():
                # Checkbox is set, start in the taskbar.
                self.__tna = True
            else:
                # Start normal.
                self.__tna = False
        if tbicon:
            # Use wx.TaskBarIcon
            self.init_tbicon()
        else:
            # Use Appindicator
            if menu:
                # Show the time not beside the indicator.
                self.__menutime = True
            else:
                # Show the time beside.
                self.__menutime = False
            wx.FutureCall(100, self.init_appind)
        # Centre window, show window.
        self.Center()
        # Check autostart
        if clock:
            # Start clock automatically.
            wx.FutureCall(200, self.clock_start)
        else:
            if self.__autostart.GetValue():
                # Checkbox is set, start clock automatically.
                wx.FutureCall(200, self.clock_start)
        if self.__tna:
            # Start in the system tray.
            self.Hide()
        else:
            self.Show()

    def clock_pause(self):
        '''Pause the clock.'''
        # stop timer
        self.__timer.Stop()
        # Show start icon, hide stop & pause icon
        self.__btnstart.Enable(True)
        self.__btnstop.Enable(True)
        self.__btnpause.Enable(False)
        self.__clockstatus = True
        # Read current time, set elapsed seconds
        timenow = int(time.time())
        self.__pausetime = timenow - self.__start
        # Remaining minutes as text.
        remain = self.get_text_minutes(self.__end - timenow)
        remain = '%s (pause)' % remain
        # Taskbar
        if self.__indstatus:
            # Application indicator
            self.__ind.set_menu_stop()
            self.__ind.set_menu_continue()
            self.__ind.set_remain_time(remain)
        else:
            # TaskBarIcon
            self.__tbicon.set_menu_stop()
            self.__tbicon.set_menu_continue()
            self.__tbicon.set_remain_time(remain)

    def clock_start(self):
        '''Start the clock.'''
        # Clock paused ?
        if self.__pausetime == -99:
            # No pause, start clock, read interval
            interval = self.get_integer_interval()
            if interval != 'dev':
                # Time interval in seconds
                self.__seconds = interval * 60.0
                # Start and end time, UTC in seconds
                self.__start = int(time.time())
                self.__end = self.__start + self.__seconds
            else:
                self.__seconds = 5.0
                self.__start = int(time.time())
                self.__end = self.__start + self.__seconds
            # Status is text notification shown.
            self.__textnotif = 'clear'
        else:
            # Clock paused, continue.
            timenow = int(time.time())
            self.__start = timenow - self.__pausetime
            self.__end = self.__start + self.__seconds
            self.__pausetime = -99
        # Start timer
        self.__timer.Start(self.__data.get_sys('wxtimer'))
        # Hide start icon, show stop & pause icon
        self.__btnstart.Enable(False)
        self.__btnstop.Enable(True)
        self.__btnpause.Enable(True)
        self.__clockstatus = True
        # Taskbar
        if self.__indstatus:
            # Application indicator
            self.__ind.set_menu_stop()
            self.__ind.set_menu_pause()
        else:
            # TaskBarIcon
            self.__tbicon.set_menu_stop()
            self.__tbicon.set_menu_pause()

    def clock_stop(self):
        '''Stop the clock.'''
        # stop timer
        self.__timer.Stop()
        # Show start icon, hide stop & pause icon
        self.__btnstart.Enable(True)
        self.__btnstop.Enable(False)
        self.__btnpause.Enable(False)
        self.__clockstatus = False
        # No pause
        self.__pausetime = -99
        # Gauge
        self.__gauge.SetValue(0)
        # Taskbar
        if self.__indstatus:
            # Application indicator
            self.__ind.set_menu_start()
            self.__ind.set_menu_pause_clear()
            self.__ind.set_remain_time('--:--')
        else:
            # TaskBarIcon
            self.__tbicon.set_menu_start()
            self.__tbicon.set_menu_pause_clear()
            self.__tbicon.set_remain_time('--:--')

    def config_load(self):
        '''Load the settings with wx.config.'''
        # Config file
        config = wx.Config(self.__data.get_sys('config_file'))
        # Get the default dictionairy as text
        textdic = self.__data.get_user_textdic()
        # Read text, textdic as default.
        newdic = config.Read(key='dic', defaultVal=textdic)
        # Set text as new dictionairy.
        self.__data.set_user_textdic(newdic)

    def config_save(self):
        '''Save the settings with wx.config.'''
        # Config file
        config = wx.Config(self.__data.get_sys('config_file'))
        # Set text notification.
        self.__data.set_user('text', self.__msgtext.GetValue())
        # Set sound notification.
        self.__data.set_user('sound', self.__sound)
        # Set time interval.
        if self.__interval != 'dev':
            self.__data.set_user('interval', self.__interval)
        # Set frame size.
        size = self.GetSize()
        self.__data.set_user('frame_size', (size[0], size[1]))
        # Set checkbox values.
        self.__data.set_user('mini_opt', self.__miniopt.GetValue())
        self.__data.set_user('autostart', self.__autostart.GetValue())
        # Get data dictionariy as text.
        textdic = self.__data.get_user_textdic()
        # Write text.
        config.Write(key='dic', value=textdic)

    def determine_path(self):
        '''Borrowed from wxglade.py, get the package directory.'''
        try:
            root = __file__
            if os.path.islink(root):
                root = os.path.realpath(root)
            return os.path.dirname(os.path.abspath(root))
        except:
            print 'I am sorry, but something is wrong.  There is no '
            print '__file__ variable. Please contact the author.'

    def get_clock(self):
        '''Get the status of the clock, True of False.'''
        return(self.__clockstatus)

    def get_integer_interval(self):
        '''Convert time interval as text to a integer value.'''
        # Get text from entry.
        text = self.__txtinterval.GetValue()
        # Error handling.
        try:
            if text != 'dev':
                interval = int(text)
            else:
                interval = text
        except ValueError:
            interval = self.__interval
        # Return integer.
        return(interval)

    def get_pause(self):
        '''Is the clock paused, True of False.'''
        if self.__pausetime == -99:
            # Clock not paused.
            status = False
        else:
            # Clock paused.
            status = True
        return(status)

    def get_text_minutes(self, seconds):
        '''Get the seconds in minutes as text, 'mm:ss'.'''
        try:
            mins = int(seconds // 60)
            secs = int(seconds % 60)
        except ValueError:
            mins, secs = 0, 0
        return('%#02d:%#02d' % (mins, secs))

    def init_appind(self):
        '''Create the application indicator.'''
        # status of the indicator.
        self.__indstatus = True
        # Application indicator.
        icon = self.__data.get_sys('indicator_icon')
        path = os.path.join(self.__dir,
                        self.__data.get_sys('indicator_path'))
        self.__ind = AppIndicator(frame=self,
                                  icon=icon,
                                  path=path,
                                  textdic={'start': _(u'Start'),
                                           'stop': _(u'Stop'),
                                           'show': _(u'Show'),
                                           'hide': _(u'Hide'),
                                           'exit': _(u'Exit'),
                                           'pause': _(u'Pause'),
                                           'cont': _(u'Continue')},
                                  menutime=self.__menutime)
        if self.__tna:
            # Start in the system tray.
            self.__ind.set_menu_show()
        self.__ind.main()

    def init_buttons(self):
        '''Create the control buttons.'''
        # Title
        t = _(u'Clock control')
        label = wx.StaticText(parent=self, label=t)
        # Start bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_start'))
        self.__btnstart = wx.BitmapButton(parent=self,
                                          bitmap=wx.Bitmap(icon))
        self.__btnstart.SetToolTip(wx.ToolTip(_(u'Start Clock')))
        # Stop bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_stop'))
        self.__btnstop = wx.BitmapButton(parent=self,
                                         bitmap=wx.Bitmap(icon))
        self.__btnstop.SetToolTip(wx.ToolTip(_(u'Clock stop')))
        # Pause bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_pause'))
        self.__btnpause = wx.BitmapButton(parent=self,
                                          bitmap=wx.Bitmap(icon))
        self.__btnpause.SetToolTip(wx.ToolTip(_(u'Clock pause')))
        # Minimize bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_minimize'))
        minimize = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        t = _(u'Minimize to Taskbar Notification Area')
        minimize.SetToolTip(wx.ToolTip(t))
        # Exit bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_exit'))
        exit_ = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        exit_.SetToolTip(wx.ToolTip(_(u'Exit Clock')))
        # Gauge to show the process.
        self.__gaugerange = self.__data.get_sys('gauge')
        self.__gauge = wx.Gauge(parent=self,
                                range=self.__gaugerange)
        # Checkbox options
        t = _(u'Start in the Taskbar Notification Area')
        self.__miniopt = wx.CheckBox(parent=self,
                                     label=t)
        t = _(u'Automatically start the clock on program startup')
        self.__autostart = wx.CheckBox(parent=self,
                                       label=t)
        # Set value from user datas.
        if self.__data.get_user('mini_opt'):
            self.__miniopt.SetValue(True)
        else:
            self.__miniopt.SetValue(False)
        if self.__data.get_user('autostart'):
            self.__autostart.SetValue(True)
        else:
            self.__autostart.SetValue(False)
        # Bindings.
        self.__btnstart.Bind(event=wx.EVT_BUTTON, handler=self.on_start)
        self.__btnstop.Bind(event=wx.EVT_BUTTON, handler=self.on_stop)
        self.__btnpause.Bind(event=wx.EVT_BUTTON, handler=self.on_pause)
        minimize.Bind(event=wx.EVT_BUTTON, handler=self.on_minimize)
        exit_.Bind(event=wx.EVT_BUTTON, handler=self.on_exit)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        vsiz.Add(item=label,
                 flag=wx.EXPAND | wx.LEFT,
                 border=self.__bdist)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        hsiz.Add(item=self.__btnstart,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=self.__btnpause,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=self.__btnstop,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.AddStretchSpacer()
        hsiz.Add(item=minimize,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=exit_,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vsiz.Add(item=hsiz, proportion=1, flag=wx.EXPAND)
        vsiz.Add(item=self.__gauge,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vsiz.Add(item=self.__miniopt,
                 flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                 border=self.__bdist)
        vsiz.Add(item=self.__autostart,
                 flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                 border=self.__bdist)
        return(vsiz)

    def init_interval(self):
        '''Create the time interval widgets.'''
        # Title
        t = _(u'Time interval in minutes')
        label = wx.StaticText(parent=self, label=t)
        # Text entry: Read default, create entry.
        self.__txtinterval = wx.TextCtrl(parent=self,
                                         value=str(self.__interval))
        # Increase bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_increase'))
        increase = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        increase.SetToolTip(wx.ToolTip(_(u'Increase time')))
        # Decrease bitmap button.
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_decrease'))
        decrease = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        decrease.SetToolTip(wx.ToolTip(_(u'Decrease time')))
        # Bindings.
        increase.Bind(event=wx.EVT_BUTTON, handler=self.on_increase)
        decrease.Bind(event=wx.EVT_BUTTON, handler=self.on_decrease)
        self.__txtinterval.Bind(event=wx.EVT_KILL_FOCUS,
                                handler=self.on_interval)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        vsiz.Add(item=label,
                 flag=wx.EXPAND | wx.LEFT,
                 border=self.__bdist)
        hsiz.Add(item=self.__txtinterval,
                 proportion=1,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=increase,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=decrease,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vsiz.Add(item=hsiz, proportion=1, flag=wx.EXPAND)
        return(vsiz)

    def init_sound(self):
        '''Create the sound notification widgets.'''
        # Title
        t = _(u'Sound notification')
        label = wx.StaticText(parent=self, label=t)
        # Sound change button
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_change'))
        change = wx.BitmapButton(parent=self,
                                 bitmap=wx.Bitmap(icon))
        change.SetToolTip(wx.ToolTip(_(u'Change sound file')))
        # Sound preview button
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('icon_preview'))
        preview = wx.BitmapButton(parent=self,
                                  bitmap=wx.Bitmap(icon))
        preview.SetToolTip(wx.ToolTip(_(u'Preview sound')))
        # Text entry, read defaults
        self.__msgsound = wx.TextCtrl(parent=self,
                                      value=self.__sound)
        # Bindings
        change.Bind(event=wx.EVT_BUTTON, handler=self.on_change)
        preview.Bind(event=wx.EVT_BUTTON, handler=self.on_preview)
        self.__msgsound.Bind(event=wx.EVT_KILL_FOCUS,
                             handler=self.on_msgsound)
        # Layout
        vsiz = wx.BoxSizer(wx.VERTICAL)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        vsiz.Add(item=label,
                 flag=wx.EXPAND | wx.LEFT,
                 border=self.__bdist)
        hsiz.Add(item=self.__msgsound,
                 proportion=1,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=change,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        hsiz.Add(item=preview,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        vsiz.Add(item=hsiz, proportion=1, flag=wx.EXPAND)
        return(vsiz)

    def init_tbicon(self):
        '''Create the wx.TaskBarIcon.'''
        self.__indstatus = False
        # TaskbarIcon
        icon = os.path.join(self.__dir,
                            self.__data.get_sys('tna_icon'))
        title = self.__data.get_sys('frame_title')
        self.__tbicon = TBIcon(frame=self,
                               icon=icon,
                               title=title,
                               textdic={'start': _(u'Start'),
                                        'stop': _(u'Stop'),
                                        'show': _(u'Show'),
                                        'hide': _(u'Hide'),
                                        'exit': _(u'Exit'),
                                        'pause': _(u'Pause'),
                                        'cont': _(u'Continue')})
        if self.__tna:
            # Start in the system tray.
            self.__tbicon.set_menu_show()

    def init_text(self):
        '''Create the text notification widgets.'''
        # Title
        t = _(u'Text notification')
        label = wx.StaticText(parent=self, label=t)
        # Text entry, read default, create entry.
        t = self.__data.get_user('text')
        self.__msgtext = wx.TextCtrl(parent=self,
                                     value=t,
                                     style=wx.TE_MULTILINE)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        vsiz.Add(item=label,
                 flag=wx.EXPAND | wx.LEFT,
                 border=self.__bdist)
        vsiz.Add(item=self.__msgtext,
                 proportion=1,
                 flag=wx.EXPAND | wx.ALL,
                 border=self.__bdist)
        return(vsiz)

    def on_change(self, event):
        '''Event for button, change sound file.'''
        # Set filename, directory path, wildcards and title.
        sfile = os.path.basename(self.__sound)
        sdir = os.path.dirname(self.__sound)
        t = _(u'file')
        w1 = 'OGG- %s (*.ogg)|*.ogg' % (t)
        w2 = 'MP3- %s (*.mp3)|*.mp3' % (t)
        w3 = 'WAV- %s (*.wav)|*.wav' % (t)
        wcard = '%s|%s|%s' % (w1, w2, w3)
        t = _(u'Select the sound file')
        # Show open dialog, get user datas.
        dlg = wx.FileDialog(parent=self,
                            message=t,
                            defaultDir=sdir,
                            defaultFile=sfile,
                            wildcard=wcard,
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # Clicked ok, set path, destroy dialog.
            path = dlg.GetPath()
            dlg.Destroy()
            # Set path to text entry and sound attribute.
            self.__sound = path
            self.__msgsound.SetValue(path)
            self.__msgsound.SetInsertionPointEnd()
        else:
            # Not clicked ok, destroy dialog.
            dlg.Destroy()

    def on_decrease(self, event):
        '''Event for bitmap button, decrease time interval.'''
        # Get interval as integer.
        interval = self.get_integer_interval()
        # decrease interval and set it to the text entry.
        self.set_integer_interval(interval - 1)

    def on_exit(self, event):
        '''Event for button, exit program.'''
        self.Close()

    def on_increase(self, event):
        '''Event for bitmap button, increase time interval.'''
        # Get interval as integer.
        interval = self.get_integer_interval()
        # decrease interval and set it to the text entry.
        self.set_integer_interval(interval + 1)

    def on_interval(self, event):
        '''Event for text control, check time interval.'''
        # Get interval as integer.
        interval = self.get_integer_interval()
        # Set interval to the text entry.
        self.set_integer_interval(interval)

    def on_minimize(self, event):
        '''Event for button, minimize frame.'''
        if self.IsShown():
            self.Hide()
            if self.__indstatus:
                # Application indicator
                self.__ind.set_menu_show()
            else:
                # wx.TaskBarIcon
                self.__tbicon.set_menu_show()

    def on_msgsound(self, event):
        '''Event for text control, check path to sound file.'''
        # Get text from entry.
        text = self.__msgsound.GetValue()
        if text:
            # Text is set, check path
            if not os.path.exists(text):
                self.__msgsound.SetValue(self.__sound)
            else:
                self.__sound = text
        else:
            # Text is not set.
            self.__sound = ''

    def on_pause(self, event):
        '''Event for button, pause the clock.'''
        self.clock_pause()

    def on_preview(self, event):
        '''Event for button, preview sound file.'''
        self.pygame_sound()

    def on_start(self, event):
        '''Event for button, start the clock.'''
        self.clock_start()

    def on_stop(self, event):
        '''Event for button, stop the clock.'''
        self.clock_stop()

    def on_system_close(self, event):
        '''Event before close the frame.'''
        if self.__lockwrite:
            # Normal program start, normal program end, delte lock file.
            self.__lock.delete_lock()
            # Close the taksbar or the indicator.
            if self.__indstatus:
                # Application indicator
                self.__ind.quit()
            elif not self.__indstatus:
                # TaskBarIcon
                self.__tbicon.Destroy()
            # Save the settings
            self.config_save()
        self.Destroy()

    def on_timer(self, event):
        '''Event for timer, the MindfulClock.'''
        timenow = int(time.time())
        if self.__textnotif == 'close':
            # Text message closed, start new interval.
            self.__start = timenow
            self.__end = self.__start + self.__seconds
            self.__gauge.SetValue(0)
            # Remaining minutes as text.
            remain = self.get_text_minutes(self.__seconds)
            # Set textnotification clear.
            self.__textnotif = 'clear'
        elif self.__textnotif == 'clear' and timenow < self.__end:
            # End is not reached.
            progress = timenow - self.__start + 1
            value = (self.__gaugerange / self.__seconds) * progress
            self.__gauge.SetValue(value)
            # Remaining minutes as text.
            remain = self.get_text_minutes(self.__end - timenow)
        elif self.__textnotif == 'clear' and timenow >= self.__end:
            # Play sound.
            self.pygame_sound()
            # Show text.
            self.show_popup()
        if self.__textnotif == 'clear':
            # Taskbar
            if self.__indstatus:
                # Application indicator
                self.__ind.set_remain_time(remain)
            else:
                # wx.TaskBarIcon
                self.__tbicon.set_remain_time(remain)
        elif self.__textnotif == 'show':
            # Taskbar
            if self.__indstatus:
                # Application indicator
                self.__ind.set_remain_time('..')
            else:
                # wx.TaskBarIcon
                self.__tbicon.set_remain_time('..')

    def pygame_sound(self):
        '''Play the 'soundfile' with Pygame.'''
        if self.__sound:
            # Soundfile is set, play sound.
            if self.__sound.endswith('.wav') or \
               self.__sound.endswith('.ogg'):
                pygame.init()
                mixer = pygame.mixer.Sound(self.__sound)
                mixer.play()
            elif self.__sound.endswith('.mp3'):
                pygame.init()
                pygame.mixer.music.load(self.__sound)
                pygame.mixer.music.play()

    def set_integer_interval(self, interval):
        '''Control value of time interval and set it to the entry.'''
        # Check interval
        if interval != 'dev':
            minimum = self.__data.get_sys('min_interval')
            maximum = self.__data.get_sys('max_interval')
            if interval < minimum:
                interval = minimum
            elif interval > maximum:
                interval = maximum
            self.__txtinterval.SetValue(str(interval))
            # Set current value as new default value.
            self.__interval = interval

    def start_question(self):
        '''Show Question, run mfc again?, return True or False.'''
        t1 = _(u'It seems the MindfulClock is running.')
        t2 = _(u'Do you want to start the clock anyway?')
        style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        dlg = wx.MessageDialog(parent=None,
                               message='%s %s' %(t1, t2),
                               caption=_(u'Start control'),
                               style=style)
        answer = dlg.ShowModal()
        if answer == wx.ID_NO:
            # Do not overwrite, return None
            status = False
        else:
            # Overwrite, return 'path'
            status = True
        return(status)

    def set_in18(self):
        '''Set the internationalization.'''
        # Get directory
        dir_ = os.path.join(self.__dir, 'locale')
        # Locale, set default language.
        self.__wxloc = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.__wxloc.AddCatalogLookupPathPrefix(dir_)
        self.__wxloc.AddCatalog('mfc1')

    def set_textnotif(self, value):
        '''Set the value of __textnotif.'''
        # Values = 'show' message on the screen, 'close' message closed,
        # 'clear' since the clock is running no message showed.
        if value in ('show', 'close', 'clear'):
            self.__textnotif = value
        else:
            self.__textnotif = None


    def show_popup(self):
        '''Show the text notification popup.'''
        text = self.__msgtext.GetValue()
        if text:
            # Text is set, show dialog.  Status of text notification.
            self.__textnotif = 'show'
            font = self.__data.get_sys('msg_font')
            colors = self.__data.get_sys('popup_colors')
            icon = os.path.join(self.__dir,
                               self.__data.get_sys('icon_close'))
            popup = Popup(parent=self,
                      style=self.__bdist,
                      text=text,
                      font=font,
                      colors=colors,
                      icon=icon)
            popw, poph = popup.get_size()
            dispw, disph = wx.GetDisplaySize()
            offx = (dispw - popw) / 2
            offy = (disph - poph) / 2
            popup.Position(ptOrigin=(0, 0), size=(offx, offy))
            popup.Popup()


if __name__ == '__main__':
    app = wx.App()
    frame = GUI(tna=False, clock=False, menu=True, tbicon=True)
    app.MainLoop()
