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
        # Name of the lock file.
        self.__name = os.path.join(path, '.mfc1_lock-%s' % userid)
        # Name of the pid file.
        self.__pid = os.path.join(path, '.mfc1_pid-%s' % userid)

    def delete_lock(self):
        '''Delete the lock, return True or False.'''
        try:
            os.remove(self.__name)
            status = True
        except OSError:
            status = False
        return(status)

    def get_pid(self, pidname):
        '''Check the linux, unix, PID, integer.'''
        # from 0 to .. numbers of running apps, -1 = no PID found.
        error = os.system('ps ax > "%s"' % self.__pid)
        if not error:
            try:
                pidfile = open(self.__pid, 'r')
                text = ''
                for i in pidfile:
                    text = '%s%s' % (text, i)
                pidfile.close()
                os.remove(self.__pid)
            except IOError:
                text = ''
        else:
            text = ''
        # Check status
        if text:
            # text is not empty.
            n = text.count(pidname)
        else:
            n = -1
        return(n)

    def is_lock(self):
        '''Check the lock, return True or False.'''
        if os.path.isfile(self.__name):
            # Lock file exists.
            status = True
        else:
            status = False
        return(status)

    def one_instance(self, scriptname):
        '''Check one instance running with lock & PID.'''
        if self.is_lock():
            # Lockfile exists, check PID.
            pid = self.get_pid(scriptname)
            if pid == 0 or pid == 1:
                status = True
            elif pid >= 2:
                status = False
            else:
                status = False
        else:
            status = True
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
