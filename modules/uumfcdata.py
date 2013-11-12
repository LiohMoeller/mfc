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


import os


class UumfcData():
    '''UumfcData()
       Data object of the Ubuntu Unity MindFulClock.

    get_(key)
    Get the data from the key.

    get_text_dic(self):
    Get the wohle dictionairy as string.

    set_(key, data)
    Set the data under the key.

    set_default(self):
    Set the default dictionairy.

    set_text_dic(self, text):
    Set the text as new dictionairy.

    '''

    def __init__(self):
        # Data dictionairy.
        self.__dic = {}
        self.set_default()

    def get_(self, key):
        '''Get the data from the 'key'.'''
        if key in self.__dic:
            data = self.__dic[key]
        else:
            data = None
        return(data)

    def get_text_dic(self):
        '''Get the wohle dictionairy as string.'''
        return(str(self.__dic))

    def set_(self, key, data):
        '''Set the data under the 'key'.'''
        key = str(key)
        self.__dic[key] = data

    def set_default(self):
        '''Set the default dictionairy.'''
        # Frame Title, icon name, frame size.
        t = 'Ubuntu Unity MindFulClock'
        self.__dic['frame_title'] = t
        self.__dic['icon_name'] = '../icons/Icon.253760.png'
        self.__dic['frame_size'] = (400, 360)
        # Message dialog, title, size, font weight, font size.
        t = 'Ubuntu Unity MindFulClock'
        self.__dic['msg_title'] = t
        self.__dic['msg_size'] = (300, 300)
        # Message dialog font = (size, family, style, weight).
        # Size = in points.
        # Family = 'decorative', 'default', 'modern', 'roman',
        #          'script', 'swiss', 'teletype'
        # Style = 'normal', 'slant', 'italic'.
        # Weight = 'normal', 'light', 'bold'.
        self.__dic['msg_font'] = (20, 'default', 'italic', 'bold')
        # Deaults: default time interval, minimal & maximal interval.
        self.__dic['def_interval'] = 30
        self.__dic['min_interval'] = 1
        self.__dic['max_interval'] = 300
        # GUI defaults: Border between widgets.
        self.__dic['gui_borderdist'] = 5
        # GUI borderstyle, 'simple', 'raised', 'sunken', 'no'
        self.__dic['gui_borderstyle'] = 'simple'
        # Icons for time interval buttons.
        self.__dic['icon_increase'] = '../icons/16/list-add.png'
        self.__dic['icon_decrease'] = '../icons/16/list-remove.png'
        # Icons for sound buttons.
        self.__dic['icon_change'] = '../icons/16/system-search.png'
        t = '../icons/16/media-playback-start.png'
        self.__dic['icon_preview'] = t
        # Icons for start, stop, minimize, exit.
        t = '../icons/32/media-playback-start.png'
        self.__dic['icon_start'] = t
        t = '../icons/32/media-playback-stop.png'
        self.__dic['icon_stop'] = t
        self.__dic['icon_minimize'] = '../icons/32/go-down.png'
        self.__dic['icon_exit'] = '../icons/32/system-log-out.png'
        # Icon for button in message dialog.
        self.__dic['icon_close'] = '../icons/32/weather-clear.png'
        # Text & sound notication.
        t = 'Please enter your message ..'
        self.__dic['text_notification'] = t
        t = '../sounds/Metal_Gong-Dianakc-109711828.wav'
        self.__dic['sound_notification'] = t
        # Value for the gauge, to show the progress.
        self.__dic['gauge'] = 100
        # Value for the wx.Timer.
        self.__dic['wxtimer'] = 100
        # Name of the config file.
        self.__dic['config_file'] = 'uumfc'

    def set_text_dic(self, text):
        '''Set the text as new dictionairy.'''
        # Convert text into a dictionairy.
        try:
            text = str(text)
            textdic = eval(text, {})
        except NameError:
            textdic = {}
        # Set default dictionairy.
        self.set_default()
        for key, value in self.__dic.items():
            if key in textdic:
                # Key exists in new dictionairy.
                newval = textdic[key]
                if key in ('frame_title',
                           'msg_title',
                           'text_notification'):
                    # Set the string as new value.
                    self.__dic[key] = str(newval)
                elif key in ('icon_name',
                             'icon_increase',
                             'icon_decrease',
                             'icon_change',
                             'icon_preview',
                             'icon_start',
                             'icon_stop',
                             'icon_minimize',
                             'icon_exit',
                             'icon_close'):
                    if os.path.exists(newval):
                        # The new file exists, set the value.
                        self.__dic[key] = newval
                elif key == 'sound_notification':
                    if newval:
                        # Soundfile is set.
                        if os.path.exists(newval):
                            # The file exists, set the value.
                            self.__dic[key] = newval
                    else:
                        # Soundfile is not set, no sound.
                        self.__dic[key] = newval
                elif key in ('frame_size',
                             'msg_size'):
                    # Check and correct the size.
                    try:
                        w, h = newval
                        w, h = int(w), int(h)
                        self.__dic[key] = (w, h)
                    except (ValueError, TypeError):
                        pass
                elif key in ('def_interval',
                             'min_interval',
                             'max_interval',
                             'gui_borderdist',
                             'gauge',
                             'wxtimer'):
                    # Check and correct the integer.
                    try:
                        n = int(newval)
                        self.__dic[key] = n
                    except (ValueError, TypeError):
                        pass
                elif key == 'gui_borderstyle':
                    # Check the border name.
                    if newval in ('simple',
                                  'raised',
                                  'sunken',
                                  'no'):
                        self.__dic[key] = newval
                elif key == 'msg_font':
                    # Check the values for the dialog fonts.
                    try:
                        osiz, ofam, osty, owei = self.__dic[key]
                        nsize, nfamily, nstyle, nweight = newval
                        nsize = int(nsize)
                        if nfamily in ('decorative',
                                       'default',
                                       'modern',
                                       'roman',
                                       'script',
                                       'swiss',
                                       'teletype'):
                            ofam = nfamily
                        if nstyle in ('normal', 'slant', 'italic'):
                            osty = nstyle
                        if nweight in ('normal', 'light', 'bold'):
                            owei = nweight
                        self.__dic[key] = (nsize, ofam, osty, owei)
                    except (ValueError, TypeError):
                        pass
