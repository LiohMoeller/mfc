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
      textdic = dictionairys with texts.  Keys = start, stop, show,
                                                 hide, exit
      menutime = True, False, show the time not beside te indicator.

    '''

    def __init__(self, frame, icon, path, textdic, menutime):
        # wx.Frame
        self.__frame = frame
        # Text dictionairy.
        self.__textdic = textdic
        # Show the time in the menu (True) or not.
        self.__menutime = menutime
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
        gtk.main()

    def menu_setup(self):
        self.menu = gtk.Menu()
        if self.__menutime:
            # Remaining time entry.
            self.remain = gtk.MenuItem('--:--')
            self.remain.show()
            self.menu.append(self.remain)
        # Clock entry.
        self.clock = gtk.MenuItem(self.__textdic['start'])
        self.clock.connect('activate', self.on_start_stop)
        self.clock.show()
        self.menu.append(self.clock)
        # GUI entry.
        self.show = gtk.MenuItem(self.__textdic['hide'])
        self.show.connect('activate', self.on_show_hide)
        self.show.show()
        self.menu.append(self.show)
        # Exit entry.
        self.exit = gtk.MenuItem(self.__textdic['exit'])
        self.exit.connect('activate', self.on_exit)
        self.exit.show()
        self.menu.append(self.exit)
        if not self.__menutime:
            # Remaining time beside the indicator icoan.
            self.ind.set_label('--:--')

    def on_exit(self, event):
        '''Event, exit the gui.'''
        self.quit()
        self.__frame.Close()

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

    def quit(self):
        '''Exit the gtk.'''
        gtk.main_quit()

    def set_menu_hide(self):
        '''Change the menu entry, hide the gui.'''
        label = self.show.child
        label.set_text(self.__textdic['hide'])

    def set_menu_show(self):
        '''Change the menu entry, show the gui.'''
        label = self.show.child
        label.set_text(self.__textdic['show'])

    def set_menu_start(self):
        '''Change the menu entry, start the clock.'''
        label = self.clock.child
        label.set_text(self.__textdic['start'])

    def set_menu_stop(self):
        '''Change the menu entry, stop the clock.'''
        label = self.clock.child
        label.set_text(self.__textdic['stop'])

    def set_remain_time(self, text):
        '''Set the remaining time.'''
        if self.__menutime:
            # Show the time in the menu.
            label = self.remain.child
            label.set_text(text)
        else:
            # Show the time beside the indicator icon.
            self.ind.set_label(text)


class wxTestFrame(wx.Frame):
    '''Test wx.Frame.

    on_launch(event)
    Test Unity application launcher.

    on_indic(event)
    Test Unity application indicator.

    '''

    def __init__(self):
        wx.Frame.__init__(self, parent=None)
        # Button
        btnlaunch = wx.Button(parent=self, label='Launcher')
        btnindic = wx.Button(parent=self, label='Indicator')
        btnexit = wx.Button(parent=self, label='Exit')
        btnlaunch.Bind(event=wx.EVT_BUTTON, handler=self.on_launch)
        btnindic.Bind(event=wx.EVT_BUTTON, handler=self.on_indic)
        btnexit.Bind(event=wx.EVT_BUTTON, handler=self.on_exit)
        # Clockstatus
        self.__clockstatus = False
        # status of the indicator.
        self.__indstatus = False
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=btnlaunch, flag=wx.EXPAND)
        vbox.Add(item=btnindic, flag=wx.EXPAND)
        vbox.Add(item=btnexit, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def clock_start(self):
        '''Start the clock.'''
        print('Start the clock ..')
        self.__clockstatus = True
        if self.__indstatus:
            self.__ind.set_menu_stop()

    def clock_stop(self):
        '''Stop the clock.'''
        print('Stop the clock ..')
        self.__clockstatus = False
        if self.__indstatus:
            self.__ind.set_menu_start()

    def get_clock(self):
        '''Get the status of the clock.'''
        return(self.__clockstatus)

    def on_exit(self, event):
        '''Event, exit button.'''
        if self.__indstatus:
            self.__ind.quit()
        self.Close()

    def on_indic(self, event):
        '''Test Unity application indicator.'''
        # status of the indicator.
        self.__indstatus = True
        # Application indicator.
        self.__ind = AppIndicator(frame=self,
                                 icon='alarm-clock-indicator',
                                 path='./icons',
                                 textdic={'start': 'Start',
                                          'stop': 'Stop',
                                          'show': 'Show',
                                          'hide': 'Hide',
                                          'exit': 'Exit'})
        self.__ind.main()

    def on_launch(self, event):
        '''Test Unity application launcher.'''

    def on_minimize(self, event):
        '''Event, minimize button.'''
        if self.IsShown():
            self.Hide()
            self.__ind.set_menu_show()

    def on_system_close(self, event):
        '''Close the clock.'''
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = wxTestFrame()
    app.MainLoop()
