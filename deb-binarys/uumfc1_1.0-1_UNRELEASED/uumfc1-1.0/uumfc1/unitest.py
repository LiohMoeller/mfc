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


import unittest
from data import Data


class Test01_UumfcData(unittest.TestCase):
    '''Unittest for uumfc1.Data().'''

    def setUp(self):
        '''Prepare test.'''
        self.__user = "{'min_interval': 1, 'gui_borderstyle': 'simple', 'sound_notification': 'sounds/Metal_Gong-Dianakc-109711828.wav', 'frame_size': (400, 360), 'icon_start': 'icons/32/media-playback-start.png', 'msg_title': 'Ubuntu Unity MindFulClock', 'icon_name': 'icons/Icon.253760.png', 'wxtimer': 100, 'gauge': 100, 'icon_close': 'icons/32/weather-clear.png', 'gui_borderdist': 5, 'msg_font': (20, 'default', 'italic', 'bold'), 'icon_increase': 'icons/16/list-add.png', 'text_notification': 'Please enter your message ..', 'config_file': 'uumfc', 'icon_stop': 'icons/32/media-playback-stop.png', 'max_interval': 300, 'def_interval': 30, 'msg_size': (300, 300), 'frame_title': 'Ubuntu Unity MindFulClock', 'icon_minimize': 'icons/32/go-down.png', 'icon_decrease': 'icons/16/list-remove.png', 'icon_change': 'icons/16/system-search.png', 'icon_preview': 'icons/16/media-playback-start.png', 'icon_exit': 'icons/32/system-log-out.png'}"

    def test_get_sys(self):
        '''Testing  uumfc1.Data.get_sys(key).'''
        data = Data()
        r = data.get_sys('config_file')
        self.failUnlessEqual(first=r, second='uumfc1')

    def test_get_user(self):
        '''Testing  uumfc1.Data.get_user(key).'''
        data = Data()
        r = data.get_user('interval')
        self.failUnlessEqual(first=r, second=30)
        r = data.get_user('text')
        self.failUnlessEqual(first=r,
                             second='Please enter your message ..')

    def test_get_user_textdic(self):
        '''Testing  uumfc1.Data.get_user_textdic().'''
        data = Data()
        r = data.get_user_textdic()
        print('UumfcData.get_user_textdic(): %s' % (r))
        self.failIfEqual(first=r, second=None)

    def test_set_user(self):
        '''Testing  uumfc1.Data.set_user(key, data).'''
        data = Data()
        r = data.set_user(key='interval', data=15.6)
        self.failUnlessEqual(first=r, second=None)
        r = data.get_user('interval')
        self.failUnlessEqual(first=r, second=15.6)
        r = data.set_user(key='text', data='Yipiehjeyeyah ..')
        self.failUnlessEqual(first=r, second=None)
        r = data.get_user('text')
        self.failUnlessEqual(first=r, second='Yipiehjeyeyah ..')

    def test_set_user_default(self):
        '''Testing  uumfc1.Data.set_user_default().'''
        data = Data()
        r = data.set_user_default()
        self.failUnlessEqual(first=r, second=None)

    def test_set_user_textdic(self):
        '''Testing  uumfc1.Data.set_user_textdic(text).'''
        data = Data()
        textdic = data.get_user_textdic()
        r = data.set_user_textdic(textdic)
        self.failUnlessEqual(first=r, second=None)
        # test with bad settings
        data.set_user('interval', 'a')
        data.set_user('frame_size', ['list'])
        data.set_user('msg_size', ('a', False))
        data.set_user('text', True)
        data.set_user('sound', 123)
        textdic = data.get_user_textdic()
        data.set_user_textdic(textdic)
        r = data.get_user('interval')
        self.failUnlessEqual(first=r, second=30)
        r = data.get_user('frame_size')
        self.failUnlessEqual(first=r, second=(400, 360))
        r = data.get_user('msg_size')
        self.failUnlessEqual(first=r, second=(300, 300))
        r = data.get_user('text')
        self.failUnlessEqual(first=r, second='True')
        r = data.get_user('sound')
        self.failUnlessEqual(first=r,
                             second='sounds/pv-bell.mp3')


if __name__ == '__main__':
    unittest.main()
