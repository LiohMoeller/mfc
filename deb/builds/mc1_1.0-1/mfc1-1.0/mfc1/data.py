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


class Data():
    '''mfc1.Data()
       Data object of the MindfulClock.

    get_sys(key)
    Get system data from the key.

    get_user(key)
    Get user data from the key.

    get_user_textdic()
    Get the user data dictionairy as string.

    set_user(key, data)
    Set user data under the key.

    set_user_default()
    Set the user data default dictionairy.

    set_user_textdic(text)
    Set the text as new user data dictionairy.

    '''

    def __init__(self):
        # System dictionairy.
        self.__sys = {}
        # Set system defaults.
        self.__sys['config_file'] = 'mfc'
        self.__sys['frame_title'] = 'MindfulClock 1.0'
        self.__sys['gauge'] = 100
        self.__sys['gui_borderdist'] = 5
        # GUI borderstyle, 'simple', 'raised', 'sunken', 'no'
        self.__sys['gui_borderstyle'] = 'simple'
        self.__sys['icon_change'] = 'icons/16/system-search.png'
        self.__sys['icon_close'] = 'icons/32/weather-clear.png'
        self.__sys['icon_decrease'] = 'icons/16/list-remove.png'
        self.__sys['icon_exit'] = 'icons/32/system-log-out.png'
        self.__sys['icon_increase'] = 'icons/16/list-add.png'
        self.__sys['icon_minimize'] = 'icons/32/go-down.png'
        self.__sys['icon_name'] = 'icons/mindfulclock.png'
        self.__sys['icon_preview'] = 'icons/16/media-playback-start.png'
        self.__sys['icon_start'] = 'icons/32/media-playback-start.png'
        self.__sys['icon_stop'] = 'icons/32/media-playback-stop.png'
        self.__sys['indicator_icon'] = 'alarm-clock-indicator'
        self.__sys['indicator_path'] = 'icons'
        self.__sys['max_interval'] = 300
        self.__sys['min_interval'] = 1
        self.__sys['msg_title'] = 'MindfulClock'
        # Message type, 'dialog' or 'popup'.
        self.__sys['msg_type'] = 'popup'
        # Popup colors, tuple with 2 colours, (text, background).
        # Colors in html format: '#RRGGBB', None for standard colour.
        self.__sys['popup_colors'] = (None, None)
        self.__sys['wxtimer'] = 100
        # Message dialog font = (size, family, style, weight).
        # Size = in points.
        # Family = 'decorative', 'default', 'modern', 'roman',
        #          'script', 'swiss', 'teletype'
        # Style = 'normal', 'slant', 'italic'.
        # Weight = 'normal', 'light', 'bold'.
        self.__sys['msg_font'] = (20, 'default', 'italic', 'bold')
        self.__sys['msg_title'] = 'MindfulClock'
        # Message type, 'dialog' or 'popup'.
        self.__sys['msg_type'] = 'popup'
        # Popup colors, tuple with 2 colours, (text, background).
        # Colors in html format: '#RRGGBB', None for standard colour.
        self.__sys['popup_colors'] = (None, None)
        self.__sys['tna_icon'] = 'icons/mindfulclock_22.png'
        self.__sys['wxtimer'] = 500
        # Set default user datas.
        self.set_user_default()

    def get_sys(self, key):
        '''Get system data from the 'key'.'''
        if key in self.__sys:
            data = self.__sys[key]
        else:
            data = None
        return(data)

    def get_user(self, key):
        '''Get user data from the 'key'.'''
        if key in self.__user:
            data = self.__user[key]
        else:
            data = None
        return(data)

    def get_user_textdic(self):
        '''Get the user data dictionairy as string.'''
        return(str(self.__user))

    def set_user(self, key, data):
        '''Set user data under the 'key'.'''
        key = str(key)
        self.__user[key] = data

    def set_user_default(self):
        '''Set the default dictionairy.'''
        # User dictionariy.
        self.__user = {}
        self.__user['frame_size'] = (400, 400)
        self.__user['msg_size'] = (300, 300)
        self.__user['interval'] = 30
        self.__user['text'] = 'Text ..'
        self.__user['sound'] = 'sounds/pv-bell.ogg'
        self.__user['mini_opt'] = False

    def set_user_textdic(self, text):
        '''Set the text as new user data dictionairy.'''
        # Convert text into a dictionairy.
        try:
            text = str(text)
            textdic = eval(text, {})
        except NameError:
            textdic = {}
        # Set default dictionairy.
        self.set_user_default()
        for key, value in self.__user.items():
            if key in textdic:
                # Key exists in new dictionairy.
                newval = textdic[key]
                if key == 'sound':
                    if newval:
                        # Soundfile is set.
                        newval = str(newval)
                        if os.path.exists(newval):
                            # The file exists, set the value.
                            self.__user[key] = newval
                    else:
                        # Soundfile is not set, no sound.
                        self.__user[key] = newval
                elif key in ('frame_size',
                             'msg_size'):
                    # Check and correct the size.
                    try:
                        w, h = newval
                        w, h = int(w), int(h)
                        self.__user[key] = (w, h)
                    except (ValueError, TypeError):
                        pass
                elif key == 'interval':
                    # Check and correct the integer.
                    try:
                        n = int(newval)
                        self.__user[key] = n
                    except (ValueError, TypeError):
                        pass
                elif key == 'text':
                    if newval:
                        # Text notification is set.
                        newval = str(newval)
                        self.__user[key] = newval
                    else:
                        # Text is not set, no text message.
                        self.__user[key] = newval
                elif key == 'mini_opt':
                    if newval:
                        # Set True
                        self.__user[key] = True
                    elif not newval:
                        # Set False
                        self.__user[key] = False
