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

    def test_set_(self):
        '''Testing  UumfcData.set_(key, data).'''
        data = UumfcData()
        r = data.set_(key='test1', data=123.7)
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key='test2', data='456kdjvnö')
        self.failUnlessEqual(first=r, second=None)
        r = data.set_(key=0xff, data=0o11)
        self.failUnlessEqual(first=r, second=None)


if __name__ == '__main__':
    unittest.main()
