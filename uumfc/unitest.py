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
    '''Unittest for uumfc.Data().'''

    def setUp(self):
        '''Prepare test.'''
        self.__textdic = "{'min_interval': 1, 'gui_borderstyle': 'simple', 'sound_notification': 'sounds/Metal_Gong-Dianakc-109711828.wav', 'frame_size': (400, 360), 'icon_start': 'icons/32/media-playback-start.png', 'msg_title': 'Ubuntu Unity MindFulClock', 'icon_name': 'icons/Icon.253760.png', 'wxtimer': 100, 'gauge': 100, 'icon_close': 'icons/32/weather-clear.png', 'gui_borderdist': 5, 'msg_font': (20, 'default', 'italic', 'bold'), 'icon_increase': 'icons/16/list-add.png', 'text_notification': 'Please enter your message ..', 'config_file': 'uumfc', 'icon_stop': 'icons/32/media-playback-stop.png', 'max_interval': 300, 'def_interval': 30, 'msg_size': (300, 300), 'frame_title': 'Ubuntu Unity MindFulClock', 'icon_minimize': 'icons/32/go-down.png', 'icon_decrease': 'icons/16/list-remove.png', 'icon_change': 'icons/16/system-search.png', 'icon_preview': 'icons/16/media-playback-start.png', 'icon_exit': 'icons/32/system-log-out.png'}"

    def test_get_(self):
        '''Testing  uumfc.Data.get_(key).'''
        data = Data()
        data.set_(key='test1', data=123.7)
        data.set_(key='test2', data='456kdjvnö')
        data.set_(key=0xff, data=0o11)
        r = data.get_('test1')
        self.failUnlessEqual(first=r, second=123.7)
        r = data.get_('test2')
        self.failUnlessEqual(first=r, second='456kdjvnö')
        r = data.get_('255')
        self.failUnlessEqual(first=r, second=0o11)

    def test_get_text_dic(self):
        '''Testing  uumfc.Data.get_text_dic().'''
        data = Data()
        r = data.get_text_dic()
        print('UumfcData.get_text_dic(): %s' % (r))
        self.failIfEqual(first=r, second=None)

    def test_set_(self):
        '''Testing  uumfc.Data.set_(key, data).'''
        data = Data()
        r = data.set_(key='test1', data=123.7)
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key='test2', data='456kdjvnö')
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key=0xff, data=0o11)
        self.failUnlessEqual(first=r, second=None)

    def test_set_default(self):
        '''Testing  uumfc.Data.set_default().'''
        data = Data()
        r = data.set_default()
        self.failUnlessEqual(first=r, second=None)

    def test_set_text_dic(self):
        '''Testing  uumfc.Data.set_text_dic(text).'''
        data = Data()
        textdic = data.get_text_dic()
        r = data.set_text_dic(textdic)
        self.failUnlessEqual(first=r, second=None)
        # test with bad settings
        data.set_('frame_title', 123)
        data.set_('icon_name', -23)
        data.set_('frame_size', 'a')
        data.set_('msg_font', ('a', 1, True, []))
        data.set_('max_interval', 'a')
        data.set_('gui_borderstyle', 'error')
        data.set_('msg_size', (50, 3000))
        data.set_('def_interval', 0)
        data.set_('min_interval', 10000)
        textdic = data.get_text_dic()
        data.set_text_dic(textdic)
        r = data.get_('frame_title')
        self.failUnlessEqual(first=r, second='123')
        r = data.get_('icon_name')
        self.failUnlessEqual(first=r, second='icons/Icon.253760.png')
        r = data.get_('frame_size')
        self.failUnlessEqual(first=r, second=(400, 360))
        r = data.get_('msg_font')
        self.failUnlessEqual(first=r,
                             second=(20, 'default', 'italic', 'bold'))
        r = data.get_('max_interval')
        self.failUnlessEqual(first=r, second=300)
        r = data.get_('gui_borderstyle')
        self.failUnlessEqual(first=r, second='simple')
        r = data.get_('msg_size')
        self.failUnlessEqual(first=r, second=(50, 3000))
        r = data.get_('def_interval')
        self.failUnlessEqual(first=r, second=0)
        r = data.get_('min_interval')
        self.failUnlessEqual(first=r, second=10000)
        data.set_text_dic('wx.Size(20, 20)')
        r = data.get_text_dic()
        self.failUnlessEqual(first=r, second=self.__textdic)


if __name__ == '__main__':
    unittest.main()
