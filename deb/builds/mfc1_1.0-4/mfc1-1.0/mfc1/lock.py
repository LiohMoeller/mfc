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


class Lock():
    '''mfc1.Lock(path, userid)

    Lock object of the MindfulClock.

    '''

    def __init__(self, path, userid):
        self.__name = os.path.join(path, '.mfc1_lock-%s' % userid)

    def delete_lock(self):
        '''Delete the lock, return True or False.'''
        try:
            os.remove(self.__name)
            status = True
        except OSError:
            status = False
        return(status)

    def is_lock(self):
        '''Check the lock, return True or False.'''
        if os.path.isfile(self.__name):
            status = True
        else:
            status = False
        return(status)

    def write_lock(self):
        '''Write the lock, return True or False.'''
        try:
            lockfile = open(self.__name, 'w')
            lockfile.write('True')
            lockfile.close()
            status = True
        except IOError:
            status = False
        return(status)
