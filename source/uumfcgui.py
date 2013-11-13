#!/usr/bin/python
# -*- coding: utf-8 -*-

# With the Unity Ubuntu MindfulClock you turn your device into a Bell
# of Mindfulness.
# Concept, Design: Marcurs Möller
#                  <marcus.moeller@outlook.com>
#                  <http://apps.microsoft.com/windows/de-de/app/
#                   mindfulclock/58063160-9cc6-4dee-9d92-17df4ce4318a>
# Programming: Andreas Ulrich
#              <ulrich3110@gmail.com>,
#              <http://erasand.jimdo.com/kontakt/>
#
# This file is part of the "Unity Ubuntu MindfulClock".
# "Unity Ubuntu MindfulClock" is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# "Unity Ubuntu MindfulClock" is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details. You should
# have received a copy of the GNU General Public License along with
# "Unity Ubuntu MindfulClock".
# If not, see <http://www.gnu.org/licenses/>.


import locale
import os
import time
import wx
import pygame
from uumfcdata import UumfcData
from uumfcmsg import UumfcMsg


# name for translations texts
_ = wx.GetTranslation


class UumfcGUI(wx.Frame):
    '''UumfcGUI()
       GUI of the Ubuntu Unity MindFulClock.

    get_integer_interval
    Convert time interval as text to a integer value.

    init_buttons(self):
    Create the control buttons.

    init_interval()
    Create the time interval widgets.

    init_sound()
    Create the sound notification widgets.

    init_text()
    Create the text notification widgets.

    on_change(event)
    Event for button, change sound file.

    on_decrease(event)
    Event for Bitmap Button, decrease time interval.

    on_exit(event)
    Event for button, exit program.

    on_increase(event)
    Event for Bitmap Button, increase time interval.

    on_interval(event)
    Event for text control, check time interval.

    on_minimize(event)
    Event for button, minimize frame.

    on_msgsound(event)
    Event for text control, check path to sound file.

    on_preview(event)
    Event for button, preview sound file.

    on_start(event)
    Event for button, start the clock.

    on_stop(event)
    Event for button, stop the clock.

    on_timer(self, event):
    Event for timer, the MindFulClock.

    pygame_sound()
    Play the soundfile with Pygame.

    set_integer_interval(interval)
    Control value of time interval and set it to the entry.

    show_dialog(self):
    Show the text notification dialogue.

    '''

    def __init__(self):
        # Data object.
        self.__data = UumfcData()
        # Load saved datas.
        self.config_load()
        # Get frame title, frame size and icon.
        title = self.__data.get_('frame_title')
        size = self.__data.get_('frame_size')
        icon = self.__data.get_('icon_name')
        # Program version.
        title = title + ' 1 / alpha'
        # Subclass
        wx.Frame.__init__(self,
                          parent=None,
                          id=wx.ID_ANY,
                          title=title,
                          size=size)
        # Icon
        if icon.endswith('.png'):
            self.SetIcon(wx.Icon(name=icon, type=wx.BITMAP_TYPE_PNG))
        # GUI border style and distance between widgets.
        bstyl = self.__data.get_('gui_borderstyle')
        guiborders = {'simple': wx.SIMPLE_BORDER,
                      'raised': wx.RAISED_BORDER,
                      'sunken': wx.SUNKEN_BORDER,
                      'no': wx.NO_BORDER}
        if bstyl in guiborders:
            self.__bstyl = guiborders[bstyl]
        else:
            self.__bstyl = wx.SIMPLE_BORDER
        self.__bdist = self.__data.get_('gui_borderdist')
        if not self.__bdist:
            self.__bdist = 5
        # Set attributes for time interval and sound file.
        self.__interval = self.__data.get_('def_interval')
        self.__sound = self.__data.get_('sound_notification')
        # Entry for time interval.  Buttons to increase or decrease
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
        # Disable stop button
        self.__btnstop.Enable(False)
        # Centre window, show window.
        self.Center()
        self.Show()

    def config_load(self):
        '''Load the settings with wx.config.'''
        # Config file
        config = wx.Config(self.__data.get_('config_file'))
        # Get the default dictionairy as text
        textdic = self.__data.get_text_dic()
        # Read text, textdic as default.
        newdic = config.Read(key='dic', defaultVal=textdic)
        # Set text as new dictionairy.
        self.__data.set_text_dic(newdic)

    def config_save(self):
        '''Save the settings with wx.config.'''
        # Config file
        config = wx.Config(self.__data.get_('config_file'))
        # Set text notification.
        self.__data.set_('text_notification', self.__msgtext.GetValue())
        # Set sound notification.
        self.__data.set_('sound_notification', self.__sound)
        # Set time interval.
        if self.__interval != 'dev':
            self.__data.set_('def_interval', self.__interval)
        # Set frame size.
        size = self.GetSize()
        self.__data.set_('frame_size', (size[0], size[1]))
        # Get data dictionariy as text.
        textdic = self.__data.get_text_dic()
        # Write text.
        config.Write(key='dic', value=textdic)

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

    def init_buttons(self):
        '''Create the control buttons.'''
        # Title
        t = _(u'Clock control.')
        label = wx.StaticText(parent=self, label=t)
        # Start bitmap button.
        icon = self.__data.get_('icon_start')
        self.__btnstart = wx.BitmapButton(parent=self,
                                          bitmap=wx.Bitmap(icon))
        self.__btnstart.SetToolTip(wx.ToolTip(_(u'Start Clock')))
        # Stop bitmap button.
        icon = self.__data.get_('icon_stop')
        self.__btnstop = wx.BitmapButton(parent=self,
                                         bitmap=wx.Bitmap(icon))
        self.__btnstop.SetToolTip(wx.ToolTip(_(u'Stop Clock')))
        # Minimize bitmap button.
        icon = self.__data.get_('icon_minimize')
        minimize = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        minimize.SetToolTip(wx.ToolTip(_(u'Minimize Clock')))
        # Exit bitmap button.
        icon = self.__data.get_('icon_exit')
        exit_ = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        exit_.SetToolTip(wx.ToolTip(_(u'Exit Clock')))
        # Gauge to show the process.
        self.__gaugerange = self.__data.get_('gauge')
        self.__gauge = wx.Gauge(parent=self,
                                range=self.__gaugerange)
        # Bindings.
        self.__btnstart.Bind(event=wx.EVT_BUTTON, handler=self.on_start)
        self.__btnstop.Bind(event=wx.EVT_BUTTON, handler=self.on_stop)
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
        return(vsiz)


    def init_interval(self):
        '''Create the time interval widgets.'''
        # Title
        t = _(u'Time interval in minutes.')
        label = wx.StaticText(parent=self, label=t)
        # Text entry: Read default, create entry.
        self.__txtinterval = wx.TextCtrl(parent=self,
                                         value=str(self.__interval))
        # Increase bitmap button.
        icon = self.__data.get_('icon_increase')
        increase = wx.BitmapButton(parent=self,
                                   bitmap=wx.Bitmap(icon))
        increase.SetToolTip(wx.ToolTip(_(u'Increase time')))
        # Decrease bitmap button.
        icon = self.__data.get_('icon_decrease')
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
        t = _(u'Sound notification.')
        label = wx.StaticText(parent=self, label=t)
        # Sound change button
        icon = self.__data.get_('icon_change')
        change = wx.BitmapButton(parent=self,
                                 bitmap=wx.Bitmap(icon))
        change.SetToolTip(wx.ToolTip(_(u'Change sound file')))
        # Sound preview button
        icon = self.__data.get_('icon_preview')
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

    def init_text(self):
        '''Create the text notification widgets.'''
        # Title
        t = _(u'Text notification.')
        label = wx.StaticText(parent=self, label=t)
        # Text entry, read default, create entry.
        t = self.__data.get_('text_notification')
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
        wcard = 'WAV- %s (*.wav)|*.wav|OGG- %s (*.ogg)|*.ogg' % (t, t)
        t = _(u'Select the sound file.')
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
        self.set_integer_interval(interval-1)

    def on_exit(self, event):
        '''Event for button, exit program.'''
        self.Close()

    def on_increase(self, event):
        '''Event for bitmap button, increase time interval.'''
        # Get interval as integer.
        interval = self.get_integer_interval()
        # decrease interval and set it to the text entry.
        self.set_integer_interval(interval+1)

    def on_interval(self, event):
        '''Event for text control, check time interval.'''
        # Get interval as integer.
        interval = self.get_integer_interval()
        # Set interval to the text entry.
        self.set_integer_interval(interval)

    def on_minimize(self, event):
        '''Event for button, minimize frame.'''
        self.Iconize()

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

    def on_preview(self, event):
        '''Event for button, preview sound file.'''
        self.pygame_sound()

    def on_start(self, event):
        '''Event for button, start the clock.'''
        # Read interval
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
        #  start timer
        self.__timer.Start(self.__data.get_('wxtimer'))
        # Hide start icon, show stop icon
        self.__btnstart.Enable(False)
        self.__btnstop.Enable(True)

    def on_stop(self, event):
        '''Event for button, stop the clock.'''
        # stop timer
        self.__timer.Stop()
        # Show start icon, hide stop icon
        self.__btnstart.Enable(True)
        self.__btnstop.Enable(False)
        self.__gauge.SetValue(0)

    def on_system_close(self, event):
        '''Event before close the frame.'''
        # Save the settings
        self.config_save()
        event.Skip()

    def on_timer(self, event):
        '''Event for timer, the MindFulClock.'''
        timenow = int(time.time())
        if timenow < self.__end:
            # End is not reached.
            progress = timenow - self.__start
            value = (self.__gaugerange / self.__seconds) * progress
            self.__gauge.SetValue(value)
        elif timenow >= self.__end:
            # End is reached, start new interval.
            self.__start = int(time.time())
            self.__end = self.__start + self.__seconds
            self.__gauge.SetValue(0)
            # Show notification, play sound.
            self.pygame_sound()
            self.show_dialog()

    def pygame_sound(self):
        '''Play the 'soundfile' with Pygame.'''
        if self.__sound:
            # Soundfile is set, play sound.
            pygame.init()
            mixer = pygame.mixer.Sound(self.__sound)
            mixer.play()

    def set_integer_interval(self, interval):
        '''Control value of time interval and set it to the entry.'''
        # Check interval
        if interval != 'dev':
            minimum = self.__data.get_('min_interval')
            maximum = self.__data.get_('max_interval')
            if interval < minimum:
                interval = minimum
            elif interval > maximum:
                interval = maximum
            self.__txtinterval.SetValue(str(interval))
            # Set current value as new default value.
            self.__interval = interval

    def show_dialog(self):
        '''Show the text notification dialogue.'''
        text = self.__msgtext.GetValue()
        if text:
            # Text is set, show dialog.
            title = self.__data.get_('msg_title')
            size = self.__data.get_('msg_size')
            icon = self.__data.get_('icon_close')
            font = self.__data.get_('msg_font')
            dlg = UumfcMsg(parent=self,
                                  title=title,
                                  size=size,
                                  icon=icon,
                                  text=text,
                                  font=font)
            dlg.ShowModal()
            # Set dialog size
            size = dlg.GetSize()
            self.__data.set_('msg_size', (size[0], size[1]))
            # Destroy dialogue.
            dlg.Destroy()


if __name__ == '__main__':
    # wxpython app
    app = wx.App()
    # internationalization of Uumfc
    wxloc = wx.Locale()
    wxloc.AddCatalogLookupPathPrefix('./in18')
    # get system language ('xx_XX', 'CHARSET')
    wxlang = locale.getdefaultlocale()
    wxlang = wxlang[0][:2]
    # get system language ('xx_XX', 'CHARSET') and select translation
    if locale.getdefaultlocale()[0][:2] == 'de':
        wxloc.AddCatalog('uumfc_de')
    # wx.frame, main loop
    frame = UumfcGUI()
    app.MainLoop()
