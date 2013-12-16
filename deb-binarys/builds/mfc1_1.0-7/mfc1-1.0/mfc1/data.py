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

    '''

    def __init__(self):
        # System dictionairy.
        self.system = {}
        # Set system defaults.
        self.system['config_file'] = 'mfc'
        self.system['frame_title'] = 'MindfulClock 1.0'
        self.system['gauge'] = 100
        self.system['gui_borderdist'] = 5
        # GUI borderstyle, 'simple', 'raised', 'sunken', 'no'
        self.system['gui_borderstyle'] = 'simple'
        self.system['icon_change'] = 'icons/16/system-search.png'
        self.system['icon_close'] = 'icons/32/weather-clear.png'
        self.system['icon_decrease'] = 'icons/16/list-remove.png'
        self.system['icon_exit'] = 'icons/32/system-log-out.png'
        self.system['icon_increase'] = 'icons/16/list-add.png'
        self.system['icon_minimize'] = 'icons/32/go-down.png'
        self.system['icon_name'] = 'icons/mindfulclock.png'
        self.system['icon_pause'] = 'icons/32/media-playback-pause.png'
        self.system['icon_preview'] = 'icons/16/media-playback-start.png'
        self.system['icon_start'] = 'icons/32/media-playback-start.png'
        self.system['icon_stop'] = 'icons/32/media-playback-stop.png'
        self.system['indicator_icon'] = 'alarm-clock-indicator'
        self.system['indicator_path'] = 'icons'
        self.system['max_interval'] = 300
        self.system['min_interval'] = 1
        # Popup colors, tuple with 2 colours, (text, background).
        # Colors in html format: '#RRGGBB', None for standard colour.
        self.system['popup_colors'] = (None, None)
        self.system['wxtimer'] = 100
        # Message dialog font = (size, family, style, weight).
        # Size = in points.
        # Family = 'decorative', 'default', 'modern', 'roman',
        #          'script', 'swiss', 'teletype'
        # Style = 'normal', 'slant', 'italic'.
        # Weight = 'normal', 'light', 'bold'.
        self.system['msg_font'] = (20, 'default', 'italic', 'bold')
        self.system['tna_icon'] = 'icons/mindfulclock_22.png'
        self.system['wxtimer'] = 500
        # Set default user datas.
        self.set_user_default()

    def set_user_default(self):
        '''Set the default dictionairy.'''
        # User dictionariy.
        self.user = {}
        self.user['frame_size'] = (400, 400)
        self.user['msg_size'] = (300, 300)
        self.user['interval'] = 30
        self.user['text'] = 'Text ..'
        self.user['sound'] = 'sounds/pv-bell.ogg'
        self.user['mini_opt'] = False
        self.user['autostart'] = False

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
        for key, value in self.user.items():
            if key in textdic:
                # Key exists in new dictionairy.
                newval = textdic[key]
                if key == 'sound':
                    if newval:
                        # Soundfile is set.
                        newval = str(newval)
                        if os.path.exists(newval):
                            # The file exists, set the value.
                            self.user[key] = newval
                    else:
                        # Soundfile is not set, no sound.
                        self.user[key] = newval
                elif key in ('frame_size',
                             'msg_size'):
                    # Check and correct the size.
                    try:
                        w, h = newval
                        w, h = int(w), int(h)
                        self.user[key] = (w, h)
                    except (ValueError, TypeError):
                        pass
                elif key == 'interval':
                    # Check and correct the integer.
                    try:
                        n = int(newval)
                        self.user[key] = n
                    except (ValueError, TypeError):
                        pass
                elif key == 'text':
                    if newval:
                        # Text notification is set.
                        newval = str(newval)
                        self.user[key] = newval
                    else:
                        # Text is not set, no text message.
                        self.user[key] = newval
                elif key in ('mini_opt', 'autostart'):
                    if newval:
                        # Set True
                        self.user[key] = True
                    elif not newval:
                        # Set False
                        self.user[key] = False
