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
    '''mfc1.TBIcon2(frame, icon, title, textdic)
       Taskbar applet for the MindfulClock.
       frame = wx.Frame
       icon = path to the icon, shown in the systray.
       title = tooltip of the systray icon.
       textdic = dictionairys with texts.  Keys = start, stop, show,
                                                  hide, exit

    '''

    def __init__(self, frame, icon, title, textdic):
        # Subclass
        wx.TaskBarIcon.__init__(self)
        # wx.Frame
        self.__frame = frame
        # Text dictionairy.
        self.__textdic = textdic
        # Systray icon
        if icon.endswith('.png'):
            trayicon = wx.Icon(icon, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon=trayicon, tooltip=title)
        # Menu
        self.init_menu()
        # Bindings
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_popup)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.on_popup)

    def init_menu(self):
        '''Create the menu.'''
        self.__menu = wx.Menu()
        # Remaining time entry.
        self.__remain = self.__menu.Append(id=wx.ID_ANY,
                                           text='--.--')
        # Clock entry.
        self.__clock = self.__menu.Append(id=wx.ID_ANY,
                                          text=self.__textdic['start'])
        self.Bind(event=wx.EVT_MENU,
                  handler=self.on_start_stop,
                  source=self.__clock)
        # GUI entry.
        self.__show = self.__menu.Append(id=wx.ID_ANY,
                                         text=self.__textdic['hide'])
        self.Bind(event=wx.EVT_MENU,
                  handler=self.on_show_hide,
                  source=self.__show)
        # Exit entry.
        self.__exit = self.__menu.Append(id=wx.ID_ANY,
                                         text=self.__textdic['exit'])
        self.Bind(event=wx.EVT_MENU,
                  handler=self.on_exit,
                  source=self.__exit)

    def on_exit(self, event):
        '''Event, start clock.'''
        self.__frame.Close()

    def on_popup(self, event):
        '''Event, show the menu.'''
        self.PopupMenu(self.__menu)

    def on_show_hide(self, event):
        '''Event, show, hide clock.'''
        if self.__frame.IsShown():
            self.__frame.Hide()
            self.set_menu_show()
        else:
            self.__frame.Show()
            self.set_menu_hide()

    def on_start_stop(self, event):
        '''Event, start, stop clock.'''
        if self.__frame.get_clock():
            # Clock is running.
            self.__frame.clock_stop()
        else:
            # Clock dont running.
            self.__frame.clock_start()

    def set_menu_hide(self):
        '''Change the menu entry, hide the gui.'''
        self.__show.SetText(self.__textdic['hide'])

    def set_menu_show(self):
        '''Change the menu entry, show the gui.'''
        self.__show.SetText(self.__textdic['show'])

    def set_menu_start(self):
        '''Change the menu entry, start the clock.'''
        self.__clock.SetText(self.__textdic['start'])

    def set_menu_stop(self):
        '''Change the menu entry, stop the clock.'''
        self.__clock.SetText(self.__textdic['stop'])

    def set_remain_time(self, text):
        '''Set the remaining time.'''
        self.__remain.SetText(text)


class wxTestFrame(wx.Frame):
    '''Test wx.Frame.

    clock_start()
    Simulate start the clock.

    clock_stop()
    Simulate stop the clock.

    '''

    def __init__(self):
        wx.Frame.__init__(self, parent=None)
        # Button
        btnmini = wx.Button(parent=self, label='Minimize')
        btnexit = wx.Button(parent=self, label='Exit')
        btnmini.Bind(event=wx.EVT_BUTTON, handler=self.on_minimize)
        btnexit.Bind(event=wx.EVT_BUTTON, handler=self.on_exit)
        # TaskbarIcon
        self.__tbicon = TBIcon(frame=self,
                               icon='icons/mindfulclock_22.png',
                               title='MindfulClock dev',
                               textdic={'start': 'Start',
                                        'stop': 'Stop',
                                        'show': 'Show',
                                        'hide': 'Hide',
                                        'exit': 'Exit'})
        self.Bind(event=wx.EVT_CLOSE,
                  handler=self.on_system_close)
        # Clock status
        self.__clockstatus = False
        # status of the indicator.
        self.__indstatus = False
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=btnmini, flag=wx.EXPAND)
        vbox.Add(item=btnexit, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def clock_start(self):
        '''Sstart the clock.'''
        print('Start the clock ..')
        self.__clockstatus = True
        if not self.__indstatus:
            self.__tbicon.set_menu_stop()

    def clock_stop(self):
        '''Stop the clock.'''
        print('Stop the clock ..')
        self.__clockstatus = False
        if not self.__indstatus:
            self.__tbicon.set_menu_start()

    def get_clock(self):
        '''Get status of the clock.'''
        return(self.__clockstatus)

    def on_exit(self, event):
        '''Event, exit button.'''
        self.Close()

    def on_minimize(self, event):
        '''Event, minimize button.'''
        if self.IsShown():
            self.Hide()
            if not self.__indstatus:
                self.__tbicon.set_menu_show()

    def on_system_close(self, event):
        '''Close the clock.'''
        self.__tbicon.Destroy()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
