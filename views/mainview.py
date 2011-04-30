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

import pygtk
import gtk
pygtk.require("2.0")

class MainView(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gtkbuilder/libreosteo-gui.glade")
        builder.connect_signals(self)
        self.windowMain = builder.get_object("windowMain")
        self.windowMain.show()

    def on_windowMain_destroy(self,widget,data=None):
      gtk.main_quit()

if __name__ == "__main__":
    print "test"
    app = MainView()
    gtk.main()
