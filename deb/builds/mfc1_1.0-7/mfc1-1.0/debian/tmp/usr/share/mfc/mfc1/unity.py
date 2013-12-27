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
# Install under unity: <sudo apt-get install python-appindicator>
import appindicator
import gtk


class AppIndicator():
    '''Application Indicator object for the MindfulClock.

    AppIndicator(rame, icon, path, textdic, menutime)
    frame = wx.Window
    icon = icon (without extension)
    path = path to icon
    textdic = dictionairys with texts.
    menutime = True, False, show the time not beside te indicator.

    '''

    def __init__(self, frame, icon, path, textdic, menutime):
        # wx.Frame
        self.frame = frame
        # Text dictionairy.
        self.textdic = textdic
        # Show the time in the menu (True) or not.
        self.menutime = menutime
        # Application indicator
        self.ind = appindicator.Indicator('MindfulClock', icon,
                               appindicator.CATEGORY_APPLICATION_STATUS,
                               path)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon(icon)
        # Gtk menu.
        self.menu_setup()
        # Set menu to the indicator.
        self.ind.set_menu(self.menu)

    def main(self):
        '''GTK main loop.'''
        gtk.main()

    def menu_setup(self):
        '''GTK menu setup.'''
        self.menu = gtk.Menu()
        if self.menutime:
            # Remaining time entry.
            self.remain = gtk.MenuItem('--:--')
            self.remain.show()
            self.menu.append(self.remain)
        # Clock entry.
        self.clock = gtk.MenuItem(self.textdic['start'])
        self.clock.connect('activate', self.on_start_stop)
        self.clock.show()
        self.menu.append(self.clock)
        # Puse entry.
        self.pause = gtk.MenuItem(self.textdic['pause'])
        self.pause.connect('activate', self.on_pause_continue)
        self.pause.show()
        self.pause.set_sensitive(False)
        self.menu.append(self.pause)
        # GUI entry.
        self.show = gtk.MenuItem(self.textdic['hide'])
        self.show.connect('activate', self.on_show_hide)
        self.show.show()
        self.menu.append(self.show)
        # Exit entry.
        self.exit = gtk.MenuItem(self.textdic['exit'])
        self.exit.connect('activate', self.on_exit)
        self.exit.show()
        self.menu.append(self.exit)
        if not self.menutime:
            # Remaining time beside the indicator icoan.
            self.ind.set_label('--:--')

    def on_exit(self, event):
        '''Event, exit the gui.'''
        self.quit_()
        self.frame.Close()

    def on_pause_continue(self, event):
        '''Event, pause, continue clock.'''
        if self.frame.get_pause():
            # Clock paused.
            self.frame.clock_start()
        elif self.frame.clockstatus:
            # Pause clock.
            self.frame.clock_pause()

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

    def quit_(self):
        '''Exit the gtk.'''
        gtk.main_quit()

    def set_menu_continue(self):
        '''Change the menu entry, clock continue.'''
        label = self.pause.child
        label.set_text(self.textdic['cont'])
        self.pause.set_sensitive(True)

    def set_menu_hide(self):
        '''Change the menu entry, hide the gui.'''
        label = self.show.child
        label.set_text(self.textdic['hide'])

    def set_menu_pause(self):
        '''Change the menu entry, clock pause.'''
        label = self.pause.child
        label.set_text(self.textdic['pause'])
        self.pause.set_sensitive(True)

    def set_menu_pause_clear(self):
        '''Change the menu entry, no pause text.'''
        label = self.pause.child
        label.set_text(self.textdic['pause'])
        self.pause.set_sensitive(False)

    def set_menu_show(self):
        '''Change the menu entry, show the gui.'''
        label = self.show.child
        label.set_text(self.textdic['show'])

    def set_menu_start(self):
        '''Change the menu entry, start the clock.'''
        label = self.clock.child
        label.set_text(self.textdic['start'])

    def set_menu_stop(self):
        '''Change the menu entry, stop the clock.'''
        label = self.clock.child
        label.set_text(self.textdic['stop'])

    def set_remain_time(self, text):
        '''Set the remaining time.'''
        if self.menutime:
            # Show the time in the menu.
            label = self.remain.child
            label.set_text(text)
        else:
            # Show the time beside the indicator icon.
            self.ind.set_label(text)


class wxTestFrame(wx.Frame):
    '''wxTestFrame()

    Test object for GUI development.

    '''

    def __init__(self):
        super(wxTestFrame, self).__init__(None)
        # Button
        btnlaunch = wx.Button(self, label='Launcher')
        btnindic = wx.Button(self, label='Indicator')
        btnexit = wx.Button(self, label='Exit')
        btnlaunch.Bind(wx.EVT_BUTTON, self.on_launch)
        btnindic.Bind(wx.EVT_BUTTON, self.on_indic)
        btnexit.Bind(wx.EVT_BUTTON, self.on_exit)
        # Clockstatus & pausetime
        self.clockstatus = False
        self.pausetime = -99
        # status of the indicator.
        self.indstatus = False
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(btnlaunch, 0, wx.EXPAND)
        vbox.Add(btnindic, 0, wx.EXPAND)
        vbox.Add(btnexit, 0, wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def clock_pause(self):
        '''Pause the clock.'''
        print('Clock pause ..')
        self.clockstatus = True
        self.pausetime = 1
        if self.indstatus:
            self.indic.set_menu_stop()
            self.indic.set_menu_continue()

    def clock_start(self):
        '''Start the clock.'''
        print('Start clock ..')
        self.clockstatus = True
        self.pausetime = -99
        if self.indstatus:
            self.indic.set_menu_stop()
            self.indic.set_menu_pause()

    def clock_stop(self):
        '''Stop the clock.'''
        print('Clock stop ..')
        self.clockstatus = False
        self.pausetime = -99
        if self.indstatus:
            self.indic.set_menu_start()
            self.indic.set_menu_pause_clear()

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
        if self.indstatus:
            self.indic.quit_()
        self.Close()

    def on_indic(self, event):
        '''Test Unity application indicator.'''
        # status of the indicator.
        self.indstatus = True
        # Application indicator.
        self.indic = AppIndicator(frame=self,
                                 icon='alarm-clock-indicator',
                                 path='./icons',
                                 textdic={'start': 'Start',
                                          'stop': 'Stop',
                                          'show': 'Show',
                                          'hide': 'Hide',
                                          'exit': 'Exit',
                                          'pause': 'Pause',
                                          'cont': 'Continue'},
                                 menutime=True)
        self.indic.main()

    def on_launch(self, event):
        '''Test Unity application launcher.'''

    def on_minimize(self, event):
        '''Event, minimize button.'''
        if self.IsShown():
            self.Hide()
            self.indic.set_menu_show()

    def on_system_close(self, event):
        '''Close the clock.'''
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
