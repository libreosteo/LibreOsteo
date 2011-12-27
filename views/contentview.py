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
import gtk
import pygtk

pygtk.require("2.0")


class ContentBuilder(object):

    def __init__(self):
        self._builder = gtk.Builder()
        self._gladefile = None

    def get_gladefile(self):
        return self._gladefile

    def set_gladefile(self, gladefile):
        self._gladefile = gladefile

    gladefile = property(get_gladefile, set_gladefile)

    def get_view(self):
        if self.gladefile is not None:
            self._builder.add_from_file(self.gladefile)
        return self._builder

    view = property(get_view)

    def attach(self, parent_view, content_name):
        content_view = self._builder.get_object(content_name)
        content_view.reparent(parent_view)


