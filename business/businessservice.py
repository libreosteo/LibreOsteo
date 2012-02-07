#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    LibreOsteo - a tool to manage osteopathy consultation
    Copyright (C) 2011  garth <garth@tuxfamily.org>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""


def internal_datalayer():
    pass

import logging
import sys


class BusinessService(object):

    def __init__(self):
        self._datalayer = internal_datalayer()
        self._logger = logging.getLogger("libreosteo.business.businessservice.BusinessService")
        self._logger.addHandler(logging.StreamHandler(sys.__stdout__))
        self.listeners = dict()

    def get_datalayer(self):
        return self._datalayer

    def get_logger(self):
        return

    def add_listener(self, listener, event):
        try:
            if listener not in self.listeners[event]:
                self.listeners[event].append(listener)
        except:
            self.listeners[event] = [listener]

    def remove_listener(self, listener, event):
        try:
            self.listeners[event].remove(listener)
        except:
            pass

    def emit(self, event, *args):
        for l in self.listeners[event]:
            if not l :
                self.remove_listener(l, event)
            try:
                l.notify(event, args)
            except:
                self._logger.error("Exception when emitting signal %s to listener %s" % (event, l), exc_info=1)
                pass
