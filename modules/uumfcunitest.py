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
from uumfcdata import UumfcData


class Test01_UumfcData(unittest.TestCase):
    '''Unittest for UumfcData().'''

    def setUp(self):
        '''Prepare test.'''
        s1 = "{'min_interval': 1, 'gui_borderstyle': 'simple', 'sound_n"
        s2 = "otification': '../sounds/Metal_Gong-Dianakc-109711828.wav"
        s3 = "', 'frame_size': (400, 360), 'icon_start': '../icons/32/m"
        s4 = "edia-playback-start.png', 'msg_title': 'Ubuntu Unity Mind"
        s5 = "FulClock', 'icon_name': '../icons/Icon.253760.png', 'wxti"
        s6 = "mer': 100, 'gauge': 100, 'icon_close': '../icons/32/weath"
        s7 = "er-clear.png', 'gui_borderdist': 5, 'msg_font': (20, 'def"
        s8 = "ault', 'italic', 'bold'), 'icon_increase': '../icons/16/l"
        s9 = "ist-add.png', 'text_notification': 'Please enter your mes"
        sa = "sage ..', 'config_file': 'uumfc', 'icon_stop': '../icons/"
        sb = "32/media-playback-stop.png', 'max_interval': 300, 'def_in"
        sc = "terval': 30, 'msg_size': (300, 300), 'frame_title': 'Ubun"
        sd = "tu Unity MindFulClock 0 / alpha', 'icon_minimize': '../ic"
        se = "ons/32/go-down.png', 'icon_decrease': '../icons/16/list-r"
        sf = "emove.png', 'icon_change': '../icons/16/system-search.png"
        sg = "', 'icon_preview': '../icons/16/media-playback-start.png'"
        sh = ", 'icon_exit': '../icons/32/system-log-out.png'}"
        self.__textdic = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + sa
        self.__textdic = self.__textdic + sb + sc + sd + se + sf + sg
        self.__textdic = self.__textdic + sh

    def test_get_(self):
        '''Testing  UumfcData.get_(key).'''
        data = UumfcData()
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
        '''Testing  UumfcData.get_text_dic().'''
        data = UumfcData()
        r = data.get_text_dic()
        self.failUnlessEqual(first=r, second=self.__textdic)

    def test_set_(self):
        '''Testing  UumfcData.set_(key, data).'''
        data = UumfcData()
        r = data.set_(key='test1', data=123.7)
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key='test2', data='456kdjvnö')
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key=0xff, data=0o11)
        self.failUnlessEqual(first=r, second=None)

    def test_set_default(self):
        '''Testing  UumfcData.set_default().'''
        data = UumfcData()
        r = data.set_default()
        self.failUnlessEqual(first=r, second=None)

    def test_set_text_dic(self):
        '''Testing  UumfcData.set_text_dic(text).'''
        data = UumfcData()
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
        self.failUnlessEqual(first=r, second='../icons/Icon.253760.png')
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
