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


import wx


# name for translations texts
_ = wx.GetTranslation


class TBIcon(wx.TaskBarIcon):
    '''mfc1.TBIcon(frame, icon, title)
       Taskbar applet for the MindFulClock.
       frame = wx.Frame
       icon = path to the icon, shown in the systray.

    '''

    def __init__(self, frame, icon, title):
        # Subclass
        wx.TaskBarIcon.__init__(self)
        # wx.Frame
        self.__frame = frame
        # Systray icon
        if icon.endswith('.png'):
            trayicon = wx.Icon(icon, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon=trayicon, tooltip=title)
        # Bindings
        self.Bind(event=wx.EVT_MENU, handler=self.on_start_stop, id=1)
        self.Bind(event=wx.EVT_MENU, handler=self.on_show_hide, id=2)
        self.Bind(event=wx.EVT_MENU, handler=self.on_exit, id=3)

    def CreatePopupMenu(self):
        '''Create and show the popup menu.'''
        menu = wx.Menu()
        if self.__frame.get_clock():
            # Clock is running.
            t = _(u'Stop')
        else:
            # Clock dont running.
            t = _(u'Start')
        menu.Append(id=1, text=t)
        if self.__frame.IsShown():
            t = _(u'Hide')
        else:
            t = _(u'Show')
        menu.Append(id=2, text=t)
        menu.Append(id=3, text=_(u'Exit'))
        return(menu)

    def on_exit(self, event):
        '''Event, start clock.'''
        self.__frame.Close()

    def on_show_hide(self, event):
        '''Event, show, hide clock.'''
        if self.__frame.IsShown():
            self.__frame.Hide()
        else:
            self.__frame.Show()

    def on_start_stop(self, event):
        '''Event, start, stop clock.'''
        if self.__frame.get_clock():
            # Clock is running.
            self.__frame.clock_stop()
        else:
            # Clock dont running.
            self.__frame.clock_start()


class wxTestFrame(wx.Frame):
    '''Test wx.Frame.

    clock_start()
    Simulate start the clock.

    clock_stop()
    Simulate stop the clock.

    '''

    def __init__(self):
        wx.Frame.__init__(self,
                          parent=None,
                          style=wx.FRAME_NO_TASKBAR | wx.RESIZE_BORDER)
        # Button
        btnmini = wx.Button(parent=self, label='Minimize')
        btnexit = wx.Button(parent=self, label='Exit')
        btnmini.Bind(event=wx.EVT_BUTTON, handler=self.on_minimize)
        btnexit.Bind(event=wx.EVT_BUTTON, handler=self.on_exit)
        # TaskbarIcon
        self.__tbicon = TBIcon(frame=self,
                               icon='icons/mindfulclock_22.png',
                               title='MindFulClock dev')
        wx.EVT_TASKBAR_LEFT_UP(self.__tbicon, self.on_tbleft)
        self.Bind(event=wx.EVT_CLOSE,
                  handler=self.on_system_close)
        # Clock status
        self.__clockstatus = False
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=btnmini, flag=wx.EXPAND)
        vbox.Add(item=btnexit, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def clock_start(self):
        '''Simulate start the clock.'''
        print('Start the clock ..')
        self.__clockstatus = True

    def clock_stop(self):
        '''Simulate stop the clock.'''
        print('Stop the clock ..')
        self.__clockstatus = False

    def get_clock(self):
        '''Simulate stop the clock.'''
        return(self.__clockstatus)

    def on_exit(self, event):
        '''Event, exit button.'''
        self.Close()

    def on_minimize(self, event):
        '''Event, minimize button.'''
        if self.IsShown():
            self.Hide()

    def on_system_close(self, event):
        '''Simulate close the clock.'''
        self.__tbicon.Destroy()
        event.Skip()

    def on_tbleft(self, event):
        '''Event, left click on the systray.'''
        #~ self.PopupMenu(self.__tbicon.CreatePopupMenu())
        if self.IsShown():
            self.Hide()
        else:
            self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
