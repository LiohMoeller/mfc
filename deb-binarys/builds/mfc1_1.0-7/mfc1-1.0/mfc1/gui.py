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


# Pygame
pygame.init()


class GUI(wx.Frame):
    '''mfc1.GUI(tna, clock, menu, tbicon)

    GUI of the MindfulClock.
    tna = True, False, start in the taskbar notification area.
    clock = True, False, start clock automatically.
    menu = True, False, show the time not beside te indicator.
    tbicon = True, False, use instead of appindicator wx.TaskBarIcon.

    '''

    def __init__(self, tna, clock, menu, tbicon):
        '''Initalize the wx.Frame.
        timer = wx.Timer

        '''
        # Init public attributes.
        self.init_public_system()
        # Internationalisation
        self.set_in18()
        # Load saved datas.
        self.config_load()
        self.init_public_user()
        # Get frame title, frame size and icon.
        title = self.data.system['frame_title']
        size = self.data.user['frame_size']
        icon = os.path.join(self.mfcdir, self.data.system['icon_name'])
        # Subclass
        super(GUI, self).__init__(None, wx.ID_ANY, title, size=size)
        # Icon
        if icon.endswith('.png'):
            self.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_PNG))
        # Initalize time interval.
        intervalbox = self.init_interval()
        # Initialize text notification.
        textbox = self.init_text()
        # Initialize Sound notification.
        soundbox = self.init_sound()
        # Ininitialize clock control.
        controlbox = self.init_buttons()
        # wx.Timer
        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        # Lock file
        self.lock_file()
        # Exit bindings.
        self.Bind(wx.EVT_CLOSE, self.on_system_close)
        # Exit when tbicon is False and __lockstate is 'exit'
        if not tbicon and self.lockstate == 'exit':
            self.Close()
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(intervalbox, 0, wx.EXPAND | wx.ALL, self.bdist)
        vbox.Add(textbox, 1, wx.EXPAND | wx.ALL, self.bdist)
        vbox.Add(soundbox, 0, wx.EXPAND | wx.ALL, self.bdist)
        vbox.Add(controlbox, 0, wx.EXPAND | wx.ALL, self.bdist)
        self.SetSizer(vbox)
        # Disable stop & pause button
        self.btnstop.Enable(False)
        self.btnpause.Enable(False)
        # Taskbar, command line option, checkbox in GUI.
        if tna:
            # Start in the taskbar.
            self.tna = True
        else:
            if self.miniopt.GetValue():
                # Checkbox is set, start in the taskbar.
                self.tna = True
            else:
                # Start normal.
                self.tna = False
        if tbicon:
            # Use wx.TaskBarIcon
            self.init_tbicon()
        else:
            # Use Appindicator
            if menu:
                # Show the time not beside the indicator.
                self.menutime = True
            else:
                # Show the time beside.
                self.menutime = False
            wx.FutureCall(100, self.init_appind)
        # Centre window, show window.
        self.Center()
        # Exit when tbicon is True and __lockstate is 'exit'
        if tbicon and self.lockstate == 'exit':
            self.Close()
        # Check autostart, command line option, check box in GUI.
        if clock:
            # Start clock automatically.
            wx.FutureCall(200, self.clock_start)
        else:
            if self.autostart.GetValue():
                # Checkbox is set, start clock automatically.
                wx.FutureCall(200, self.clock_start)
        if self.tna:
            # Start in the system tray.
            self.Hide()
        else:
            self.Show()

    def clock_pause(self):
        '''Pause the clock.'''
        # stop timer
        self.timer.Stop()
        # Show start icon, hide stop & pause icon
        self.btnstart.Enable(True)
        self.btnstop.Enable(True)
        self.btnpause.Enable(False)
        self.clockstatus = True
        # Read current time, set elapsed seconds
        timenow = int(time.time())
        self.pausetime = timenow - self.start
        # Remaining minutes as text.
        remain = self.get_text_minutes(self.end - timenow)
        remain = '%s (pause)' % remain
        # Taskbar
        if self.tbtype == 'appind':
            # Application indicator
            self.indic.set_menu_stop()
            self.indic.set_menu_continue()
            self.indic.set_remain_time(remain)
        elif self.tbtype == 'tbicon':
            # TaskBarIcon
            self.tbicon.set_menu_stop()
            self.tbicon.set_menu_continue()
            self.tbicon.set_remain_time(remain)

    def clock_start(self):
        '''Start the clock.'''
        # Clock paused ?
        if self.pausetime == -99:
            # No pause, start clock, read interval
            interval = self.get_integer_interval()
            if interval != 'dev':
                # Time interval in seconds
                self.seconds = interval * 60.0
                # Start and end time, UTC in seconds
                self.start = int(time.time())
                self.end = self.start + self.seconds
            else:
                self.seconds = 5.0
                self.start = int(time.time())
                self.end = self.start + self.seconds
            # Status text notification & sound.
            self.textnotif = 'clear'
            self.soundplay = 'clear'
        else:
            # Clock paused, continue.
            timenow = int(time.time())
            self.start = timenow - self.pausetime
            self.end = self.start + self.seconds
            self.pausetime = -99
        # Start timer
        self.timer.Start(self.data.system['wxtimer'])
        # Hide start icon, show stop & pause icon
        self.btnstart.Enable(False)
        self.btnstop.Enable(True)
        self.btnpause.Enable(True)
        self.clockstatus = True
        # Taskbar
        if self.tbtype == 'appind':
            # Application indicator
            self.indic.set_menu_stop()
            self.indic.set_menu_pause()
        elif self.tbtype == 'tbicon':
            # TaskBarIcon
            self.tbicon.set_menu_stop()
            self.tbicon.set_menu_pause()

    def clock_stop(self):
        '''Stop the clock.'''
        # stop timer
        self.timer.Stop()
        # Show start icon, hide stop & pause icon
        self.btnstart.Enable(True)
        self.btnstop.Enable(False)
        self.btnpause.Enable(False)
        self.clockstatus = False
        # No pause
        self.pausetime = -99
        # Gauge
        self.gauge.SetValue(0)
        # Taskbar
        if self.tbtype == 'appind':
            # Application indicator
            self.indic.set_menu_start()
            self.indic.set_menu_pause_clear()
            self.indic.set_remain_time('--:--')
        elif self.tbtype == 'tbicon':
            # TaskBarIcon
            self.tbicon.set_menu_start()
            self.tbicon.set_menu_pause_clear()
            self.tbicon.set_remain_time('--:--')

    def config_load(self):
        '''Load the settings with wx.config.'''
        # Config file
        config = wx.Config(self.data.system['config_file'])
        # Get the default dictionairy as text
        deftextdic = str(self.data.user)
        # Read new text, textdic as default.
        newtextdic = config.Read(key='dic', defaultVal=deftextdic)
        # Set new text as new dictionairy.
        self.data.set_user_textdic(newtextdic)

    def config_save(self):
        '''Save the settings with wx.config.'''
        # Config file
        config = wx.Config(self.data.system['config_file'])
        # Set text notification.
        self.data.user['text'] = self.msgtext.GetValue()
        # Set sound notification.
        self.data.user['sound'] = self.sound
        # Set time interval.
        if self.interval != 'dev':
            self.data.user['interval'] = self.interval
        # Set frame size.
        size = self.GetSize()
        self.data.user['frame_size'] = (size[0], size[1])
        # Set checkbox values.
        self.data.user['mini_opt'] = self.miniopt.GetValue()
        self.data.user['autostart'] = self.autostart.GetValue()
        # Get data dictionariy as text.
        textdic = str(self.data.user)
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
            print('There is no __file__ variable.')

    def get_integer_interval(self):
        '''Convert time interval as text to a integer value.'''
        # Get text from entry.
        text = self.txtinterval.GetValue()
        # Error handling.
        try:
            if text != 'dev':
                interval = int(text)
            else:
                interval = text
        except ValueError:
            interval = self.interval
        # Return integer.
        return(interval)

    def get_pause(self):
        '''Is the clock paused, True of False.'''
        if self.pausetime == -99:
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
        '''Create the application indicator. Public objects:
        indic = mfc1.AppIndicator

        '''
        # status of the indicator.
        self.tbtype = 'appind'
        # Application indicator.
        icon = self.data.system['indicator_icon']
        path = os.path.join(self.mfcdir,
                        self.data.system['indicator_path'])
        self.indic = AppIndicator(frame=self,
                                  icon=icon,
                                  path=path,
                                  textdic={'start': _(u'Start'),
                                           'stop': _(u'Stop'),
                                           'show': _(u'Show'),
                                           'hide': _(u'Hide'),
                                           'exit': _(u'Exit'),
                                           'pause': _(u'Pause'),
                                           'cont': _(u'Continue')},
                                  menutime=self.menutime)
        if self.tna:
            # Start in the system tray.
            self.indic.set_menu_show()
        self.indic.main()

    def init_buttons(self):
        '''Create the control buttons. Public widgets:
        btnstart = wx.BitmapButton
        btnstop = wx.BitmapButton
        btnpause = wx.BitmapButton
        gauge = wx.Gauge
        miniopt = wx.CheckBox
        autostart = wx.CheckBox

        '''
        # Title
        t = _(u'Clock control')
        label = wx.StaticText(self, label=t)
        # Start bitmap button.
        icon = os.path.join(self.mfcdir, self.data.system['icon_start'])
        self.btnstart = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        self.btnstart.SetToolTip(wx.ToolTip(_(u'Start Clock')))
        # Stop bitmap button.
        icon = os.path.join(self.mfcdir, self.data.system['icon_stop'])
        self.btnstop = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        self.btnstop.SetToolTip(wx.ToolTip(_(u'Clock stop')))
        # Pause bitmap button.
        icon = os.path.join(self.mfcdir, self.data.system['icon_pause'])
        self.btnpause = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        self.btnpause.SetToolTip(wx.ToolTip(_(u'Clock pause')))
        # Minimize bitmap button.
        icon = os.path.join(self.mfcdir,
                            self.data.system['icon_minimize'])
        minimize = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        t = _(u'Minimize to Taskbar Notification Area')
        minimize.SetToolTip(wx.ToolTip(t))
        # Exit bitmap button.
        icon = os.path.join(self.mfcdir, self.data.system['icon_exit'])
        exit_ = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        exit_.SetToolTip(wx.ToolTip(_(u'Exit Clock')))
        # Gauge to show the process.
        self.gauge = wx.Gauge(self, range=self.gaugerange)
        # Checkbox options
        t = _(u'Start in the Taskbar Notification Area')
        self.miniopt = wx.CheckBox(self, label=t)
        t = _(u'Automatically start the clock on program startup')
        self.autostart = wx.CheckBox(self, label=t)
        # Set value from user datas.
        if self.data.user['mini_opt']:
            self.miniopt.SetValue(True)
        else:
            self.miniopt.SetValue(False)
        if self.data.user['autostart']:
            self.autostart.SetValue(True)
        else:
            self.autostart.SetValue(False)
        # Bindings.
        self.btnstart.Bind(wx.EVT_BUTTON, self.on_start)
        self.btnstop.Bind(wx.EVT_BUTTON, self.on_stop)
        self.btnpause.Bind(wx.EVT_BUTTON, self.on_pause)
        minimize.Bind(wx.EVT_BUTTON, self.on_minimize)
        exit_.Bind(wx.EVT_BUTTON, self.on_exit)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        vsiz.Add(label, 0, wx.EXPAND | wx.LEFT, self.bdist)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        hsiz.Add(self.btnstart, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(self.btnpause, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(self.btnstop, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.AddStretchSpacer()
        hsiz.Add(minimize, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(exit_, 0, wx.EXPAND | wx.ALL, self.bdist)
        vsiz.Add(hsiz, 1, wx.EXPAND)
        vsiz.Add(self.gauge, 0, wx.EXPAND | wx.ALL, self.bdist)
        vsiz.Add(self.miniopt,
                 0,
                 wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                 self.bdist)
        vsiz.Add(self.autostart,
                 0,
                 wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                 self.bdist)
        return(vsiz)

    def init_interval(self):
        '''Create the time interval widgets. Public widgets:
        txtinterval = wx.TextCtrl

        '''
        # Title
        t = _(u'Time interval in minutes')
        label = wx.StaticText(self, label=t)
        # Text entry: Read default, create entry.
        self.txtinterval = wx.TextCtrl(self, value=str(self.interval))
        # Increase bitmap button.
        icon = os.path.join(self.mfcdir,
                            self.data.system['icon_increase'])
        increase = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        increase.SetToolTip(wx.ToolTip(_(u'Increase time')))
        # Decrease bitmap button.
        icon = os.path.join(self.mfcdir,
                            self.data.system['icon_decrease'])
        decrease = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        decrease.SetToolTip(wx.ToolTip(_(u'Decrease time')))
        # Bindings.
        increase.Bind(wx.EVT_BUTTON, self.on_increase)
        decrease.Bind(wx.EVT_BUTTON, self.on_decrease)
        self.txtinterval.Bind(wx.EVT_KILL_FOCUS, self.on_interval)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        vsiz.Add(label, 0, wx.EXPAND | wx.LEFT, self.bdist)
        hsiz.Add(self.txtinterval, 1, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(increase, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(decrease, 0, wx.EXPAND | wx.ALL, self.bdist)
        vsiz.Add(hsiz, 1, wx.EXPAND)
        return(vsiz)

    def init_public_system(self):
        '''Initialize public system attributes.
        data = Data object, mfc1.Data()
        mfcdir = Path of the package mfc1, string.
        bstyl = GUI border style, wx.BORDER.
        bdist = GUI distance between widgets, integer.
        clockstatus = Clock is running, True or False.
        tbtype = Type of Taskbar Notification, string.
            'appind' = application indicator
            'tbicon' = taskbaricon
            '' = no taskbar started.
        textnotif = Status of the text notification, string.
            'show' message on the screen
            'close' message closed,
            'clear' since the clock is running no message showed.
        playsound = Status of the sound message, string.
            'clear' = since the clock is running no sound played,
            'close' = sound finished.,
            'play-sound' = play wav or ogg
            'play-music' = play mp3
        pausetime >= 0:   clock is paused, elapsed time.
                  == -99: clock is not paused.

        '''
        self.data = Data()
        self.mfcdir = self.determine_path()
        # bstyl
        bstyl = self.data.system['gui_borderstyle']
        guiborders = {'simple': wx.SIMPLE_BORDER,
                      'raised': wx.RAISED_BORDER,
                      'sunken': wx.SUNKEN_BORDER,
                      'no': wx.NO_BORDER}
        if bstyl in guiborders:
            self.bstyl = guiborders[bstyl]
        else:
            self.bstyl = wx.SIMPLE_BORDER
        # bdist
        self.bdist = self.data.system['gui_borderdist']
        # gaugerange, clockstatus, tbtype.
        self.gaugerange = self.data.system['gauge']
        self.clockstatus = False
        self.tbtype = ''
        # textnotif, soundplay, pausetime.
        self.textnotif = 'clear'
        self.soundplay = 'clear'
        self.pausetime = -99

    def init_public_user(self):
        '''Initialize public user datas.
        interval = Interval in seconds, integer.
        sound = Path to sound, music, file, string.

        '''
        self.interval = self.data.user['interval']
        s = self.data.user['sound']
        if s:
            self.sound = os.path.join(self.mfcdir, s)
        else:
            self.sound = ''

    def init_sound(self):
        '''Create the sound notification widgets. Public objects:
        msgsound = wx.TextCtrl

        '''
        # Title
        t = _(u'Sound notification')
        label = wx.StaticText(self, label=t)
        # Sound change button
        icon = os.path.join(self.mfcdir,
                            self.data.system['icon_change'])
        change = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        change.SetToolTip(wx.ToolTip(_(u'Change sound file')))
        # Sound preview button
        icon = os.path.join(self.mfcdir,
                            self.data.system['icon_preview'])
        preview = wx.BitmapButton(self, bitmap=wx.Bitmap(icon))
        preview.SetToolTip(wx.ToolTip(_(u'Preview sound')))
        # Text entry, read defaults
        self.msgsound = wx.TextCtrl(self, value=self.sound)
        # Bindings
        change.Bind(wx.EVT_BUTTON, self.on_change)
        preview.Bind(wx.EVT_BUTTON, self.on_preview)
        self.msgsound.Bind(wx.EVT_KILL_FOCUS, self.on_msgsound)
        # Layout
        vsiz = wx.BoxSizer(wx.VERTICAL)
        hsiz = wx.BoxSizer(wx.HORIZONTAL)
        vsiz.Add(label, 0, wx.EXPAND | wx.LEFT, self.bdist)
        hsiz.Add(self.msgsound, 1, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(change, 0, wx.EXPAND | wx.ALL, self.bdist)
        hsiz.Add(preview, 0, wx.EXPAND | wx.ALL, self.bdist)
        vsiz.Add(hsiz, 1, wx.EXPAND)
        return(vsiz)

    def init_tbicon(self):
        '''Create the wx.TaskBarIcon. Public objects:
        tbicon = mfc1.TBIcon

        '''
        self.tbtype = 'tbicon'
        # TaskbarIcon
        icon = os.path.join(self.mfcdir,
                            self.data.system['tna_icon'])
        title = self.data.system['frame_title']
        self.tbicon = TBIcon(frame=self,
                             icon=icon,
                             title=title,
                             textdic={'start': _(u'Start'),
                                      'stop': _(u'Stop'),
                                      'show': _(u'Show'),
                                      'hide': _(u'Hide'),
                                      'exit': _(u'Exit'),
                                      'pause': _(u'Pause'),
                                      'cont': _(u'Continue')})
        if self.tna:
            # Start in the system tray.
            self.tbicon.set_menu_show()

    def init_text(self):
        '''Create the text notification widgets. Public widgets:
        msgtext = wx.TextCtrl

        '''
        # Title
        t = _(u'Text notification')
        label = wx.StaticText(self, label=t)
        # Text entry, read default, create entry.
        t = self.data.user['text']
        self.msgtext = wx.TextCtrl(self,
                                     value=t,
                                     style=wx.TE_MULTILINE)
        # Layout.
        vsiz = wx.BoxSizer(wx.VERTICAL)
        vsiz.Add(label, 0, wx.EXPAND | wx.LEFT, self.bdist)
        vsiz.Add(self.msgtext, 1, wx.EXPAND | wx.ALL, self.bdist)
        return(vsiz)

    def lock_file(self):
        '''Handle the mc1.Lock object. Public objects:
        lock = mfc1.Lock
        lockstate = Status of the lock file.
                    '' = No status.
                    'written' = Lock file is written
                    'deleted' = Lock file is deleted
                    'exit' = Program exit

        '''
        userid = wx.GetUserId()
        wxpath = wx.StandardPaths.Get()
        userdir = wxpath.GetDocumentsDir()
        self.lock = Lock(path=userdir, userid=userid)
        self.lockstate = ''
        if self.lock.one_instance('mindfulclock1'):
            # One instance.
            self.lock.write_lock()
            self.lockstate = 'written'
        else:
            # More than one instance.
            if self.start_question():
                # Start the clock.
                self.lock.write_lock()
                self.lockstate = 'written'
            else:
                # Exit the program.
                self.lockstate = 'exit'

    def on_change(self, event):
        '''Event for button, change sound file.'''
        # Set filename, directory path, wildcards and title.
        t = _(u'file')
        w1 = 'OGG- %s (*.ogg)|*.ogg' % (t)
        w2 = 'MP3- %s (*.mp3)|*.mp3' % (t)
        w3 = 'WAV- %s (*.wav)|*.wav' % (t)
        #~ wcard =
        # Show open dialog, get user datas.
        dlg = wx.FileDialog(self,
                            _(u'Select the sound file'),
                            os.path.dirname(self.sound),
                            os.path.basename(self.sound),
                            '%s|%s|%s' % (w1, w2, w3),
                            wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # Clicked ok, set path, destroy dialog.
            path = dlg.GetPath()
            dlg.Destroy()
            # Set path to text entry and sound attribute.
            self.sound = path
            self.msgsound.SetValue(path)
            self.msgsound.SetInsertionPointEnd()
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
            if self.tbtype == 'appind':
                # Application indicator
                self.indic.set_menu_show()
            elif self.tbtype == 'tbicon':
                # wx.TaskBarIcon
                self.tbicon.set_menu_show()

    def on_msgsound(self, event):
        '''Event for text control, check path to sound file.'''
        # Get text from entry.
        text = self.msgsound.GetValue()
        if text:
            # Text is set, check path
            if not os.path.exists(text):
                self.msgsound.SetValue(self.sound)
            else:
                self.sound = text
        else:
            # Text is not set.
            self.sound = ''

    def on_pause(self, event):
        '''Event for button, pause the clock.'''
        self.clock_pause()

    def on_preview(self, event):
        '''Event for button, preview sound file.'''
        self.pygame_sound(True)

    def on_start(self, event):
        '''Event for button, start the clock.'''
        self.config_save()
        self.clock_start()

    def on_stop(self, event):
        '''Event for button, stop the clock.'''
        self.clock_stop()

    def on_system_close(self, event):
        '''Event before close the frame.'''
        if self.lockstate == 'written':
            # Normal program start, normal program end,
            # delete lock file.
            self.lock.delete_lock()
            self.lockstate = 'deleted'
        # Close the taksbar or the indicator.
        if self.tbtype == 'appind':
            # Application indicator
            self.indic.quit_()
        elif self.tbtype == 'tbicon':
            # TaskBarIcon
            self.tbicon.Destroy()
        # Save the settings
        self.config_save()
        self.Destroy()

    def on_timer(self, event):
        '''Event for timer, the MindfulClock.'''
        timenow = int(time.time())
        if self.textnotif == 'close' and self.soundplay == 'close':
            # Text message & sound closed, start new interval.
            self.start = timenow
            self.end = self.start + self.seconds
            self.gauge.SetValue(0)
            # Remaining minutes as text.
            remain = self.get_text_minutes(self.seconds)
            # Set text notification & sound clear.
            self.textnotif = 'clear'
            self.soundplay = 'clear'
        elif self.textnotif == 'clear' and \
             self.soundplay == 'clear' and timenow < self.end:
            # End is not reached.
            progress = timenow - self.start + 1
            value = (self.gaugerange / self.seconds) * progress
            self.gauge.SetValue(value)
            # Remaining minutes as text.
            remain = self.get_text_minutes(self.end - timenow)
        elif self.textnotif == 'clear' and \
             self.soundplay == 'clear' and timenow >= self.end:
            # Play sound.
            self.pygame_sound(False)
            # Show text.
            self.show_popup()
        if self.textnotif == 'clear' and self.soundplay == 'clear':
            # Taskbar
            if self.tbtype == 'appind':
                # Application indicator
                self.indic.set_remain_time(remain)
            elif self.tbtype == 'tbicon':
                # wx.TaskBarIcon
                self.tbicon.set_remain_time(remain)
        elif self.textnotif == 'show' or \
             self.soundplay.startswith('play'):
            # Taskbar
            if self.tbtype == 'appind':
                # Application indicator
                self.indic.set_remain_time('..')
            elif self.tbtype == 'tbicon':
                # wx.TaskBarIcon
                self.tbicon.set_remain_time('..')
        # Check sound.
        if self.soundplay == 'play-sound':
            # wav or ogg
            if not pygame.mixer.get_busy():
                self.soundplay = 'close'
        elif self.soundplay == 'play-music':
            # mp3
            if not pygame.mixer.music.get_busy():
                self.soundplay = 'close'

    def pygame_sound(self, preview):
        '''Play the 'soundfile' with Pygame, preview= True or False.'''
        # preview = False: Clock stop while playing sound or music.
        # preview = True: No interrupt of the clock.
        if self.sound:
            # Soundfile is set, play sound.
            if self.sound.endswith('.wav') or \
               self.sound.endswith('.ogg'):
                mixer = pygame.mixer.Sound(self.sound)
                mixer.play()
                if not preview:
                    self.soundplay = 'play-sound'
            elif self.sound.endswith('.mp3'):
                pygame.mixer.music.load(self.sound)
                pygame.mixer.music.play()
                if not preview:
                    self.soundplay = 'play-music'
        else:
            # No sound, set __soundplay 'close'.
            self.soundplay = 'close'


    def set_integer_interval(self, interval):
        '''Control value of time interval and set it to the entry.'''
        # Check interval
        if interval != 'dev':
            minimum = self.data.system['min_interval']
            maximum = self.data.system['max_interval']
            if interval < minimum:
                interval = minimum
            elif interval > maximum:
                interval = maximum
            self.txtinterval.SetValue(str(interval))
            # Set current value as new default value.
            self.interval = interval

    def start_question(self):
        '''Show Question, run mfc again?, return True or False.'''
        t1 = _(u'It seems the MindfulClock is running.')
        t2 = _(u'Do you want to start the clock anyway?')
        style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        dlg = wx.MessageDialog(None,
                               '%s %s' %(t1, t2),
                               _(u'Start control'),
                               style)
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
        dir_ = os.path.join(self.mfcdir, 'locale')
        # Locale, set default language.
        self.wxloc = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.wxloc.AddCatalogLookupPathPrefix(dir_)
        self.wxloc.AddCatalog('mfc1')

    def show_popup(self):
        '''Show the text notification popup.'''
        text = self.msgtext.GetValue()
        if text:
            # Text is set, show dialog.  Status of text notification.
            self.textnotif = 'show'
            font = self.data.system['msg_font']
            colors = self.data.system['popup_colors']
            icon = os.path.join(self.mfcdir,
                               self.data.system['icon_close'])
            popup = Popup(parent=self,
                      style=self.bdist,
                      text=text,
                      font=font,
                      colors=colors,
                      icon=icon)
            popw, poph = popup.size
            dispw, disph = wx.GetDisplaySize()
            offx = (dispw - popw) / 2
            offy = (disph - poph) / 2
            popup.Position(ptOrigin=(0, 0), size=(offx, offy))
            popup.Popup()
        else:
            # No text, no Popup, set __textnotif 'close'.
            self.textnotif = 'close'


if __name__ == '__main__':
    app = wx.App()
    frame = GUI(tna=False, clock=False, menu=True, tbicon=False)
    app.MainLoop()
