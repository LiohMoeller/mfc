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
    icon = path to the icon, shown in the taskbar notification area.
    title = tooltip of the takskbar icon.
    textdic = dictionairys with texts.

    '''

    def __init__(self, frame, icon, title, textdic):
        # Subclass
        wx.TaskBarIcon.__init__(self)
        # wx.Frame
        self.frame = frame
        # Text dictionairy.
        self.textdic = textdic
        # taskbar icon
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
        self.menu = wx.Menu()
        # Remaining time entry.
        self.remain = self.menu.Append(wx.ID_ANY, '--.--')
        # Clock entry.
        self.clock = self.menu.Append(wx.ID_ANY,
                                          self.textdic['start'])
        self.Bind(wx.EVT_MENU, self.on_start_stop, self.clock)
        # Pause entry.
        self.pause = self.menu.Append(wx.ID_ANY,
                                          self.textdic['pause'])
        self.pause.Enable(False)
        self.Bind(wx.EVT_MENU, self.on_pause_continue, self.pause)
        # GUI entry.
        self.show = self.menu.Append(wx.ID_ANY,
                                         self.textdic['hide'])
        self.Bind(wx.EVT_MENU, self.on_show_hide, self.show)
        # Exit entry.
        self.exit_ = self.menu.Append(wx.ID_ANY,
                                         self.textdic['exit'])
        self.Bind(wx.EVT_MENU, handler=self.on_exit, source=self.exit_)

    def on_exit(self, event):
        '''Event, exit the gui.'''
        self.frame.Close()

    def on_pause_continue(self, event):
        '''Event, pause, continue clock.'''
        if self.frame.get_pause():
            # Clock paused.
            self.frame.clock_start()
        elif self.frame.clockstatus:
            # Pause clock.
            self.frame.clock_pause()

    def on_popup(self, event):
        '''Event, show the menu.'''
        self.PopupMenu(self.menu)

    def on_show_hide(self, event):
        '''Event, show, hide clock.'''
        if self.frame.IsShown():
            self.frame.Hide()
            self.set_menu_show()
        else:
            self.frame.Show()
            self.set_menu_hide()

    def on_start_stop(self, event):
        '''Event, start, stop clock.'''
        if self.frame.clockstatus:
            # Clock is running.
            self.frame.clock_stop()
        else:
            # Clock dont running.
            self.frame.clock_start()

    def set_menu_continue(self):
        '''Change the menu entry, clock continue.'''
        self.pause.SetText(self.textdic['cont'])
        self.pause.Enable(True)

    def set_menu_hide(self):
        '''Change the menu entry, hide the gui.'''
        self.show.SetText(self.textdic['hide'])

    def set_menu_pause(self):
        '''Change the menu entry, clock pause.'''
        self.pause.SetText(self.textdic['pause'])
        self.pause.Enable(True)

    def set_menu_pause_clear(self):
        '''Change the menu entry, no pause text.'''
        self.pause.SetText(self.textdic['pause'])
        self.pause.Enable(False)

    def set_menu_show(self):
        '''Change the menu entry, show the gui.'''
        self.show.SetText(self.textdic['show'])

    def set_menu_start(self):
        '''Change the menu entry, start the clock.'''
        self.clock.SetText(self.textdic['start'])

    def set_menu_stop(self):
        '''Change the menu entry, stop the clock.'''
        self.clock.SetText(self.textdic['stop'])

    def set_remain_time(self, text):
        '''Set the remaining time.'''
        self.remain.SetText(text)


class wxTestFrame(wx.Frame):
    '''wxTestFrame()

    Test object for GUI development.

    '''

    def __init__(self):
        super(wxTestFrame, self).__init__(None)
        # Button
        btnmini = wx.Button(parent=self, label='Minimize')
        btnexit = wx.Button(parent=self, label='Exit')
        btnmini.Bind(wx.EVT_BUTTON, self.on_minimize)
        btnexit.Bind(wx.EVT_BUTTON, self.on_exit)
        # TaskbarIcon
        self.tbicon = TBIcon(frame=self,
                               icon='icons/mindfulclock_22.png',
                               title='MindfulClock dev',
                               textdic={'start': 'Start',
                                        'stop': 'Stop',
                                        'show': 'Show',
                                        'hide': 'Hide',
                                        'exit': 'Exit',
                                        'pause': 'Pause',
                                        'cont': 'Continue'})
        self.Bind(wx.EVT_CLOSE, self.on_system_close)
        # Clock status
        self.clockstatus = False
        # status of the indicator.
        self.indstatus = False
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(btnmini, 0, wx.EXPAND)
        vbox.Add(btnexit, 0, wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def clock_pause(self):
        '''Pause the clock.'''
        print('Clock pause ..')
        self.clockstatus = True
        self.pausetime = 1
        if not self.indstatus:
            self.tbicon.set_menu_stop()
            self.tbicon.set_menu_continue()

    def clock_start(self):
        '''Start the clock.'''
        print('Start the clock ..')
        self.clockstatus = True
        self.pausetime = -99
        if not self.indstatus:
            self.tbicon.set_menu_stop()
            self.tbicon.set_menu_pause()

    def clock_stop(self):
        '''Stop the clock.'''
        print('Stop the clock ..')
        self.clockstatus = False
        self.pausetime = -99
        if not self.indstatus:
            self.tbicon.set_menu_start()
            self.tbicon.set_menu_pause_clear()

    def get_pause(self):
        '''Is the clock paused, True of False.'''
        if self.pausetime == -99:
            # Clock not paused.
            status = False
        else:
            # Clock paused.
            status = True
        return(status)

    def on_exit(self, event):
        '''Event, exit button.'''
        self.Close()

    def on_minimize(self, event):
        '''Event, minimize button.'''
        if self.IsShown():
            self.Hide()
            if not self.indstatus:
                self.tbicon.set_menu_show()

    def on_system_close(self, event):
        '''Close the clock.'''
        self.tbicon.Destroy()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
