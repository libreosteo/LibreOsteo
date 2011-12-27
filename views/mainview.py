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
from views.addpatientcontent import AddPatientContent
from views.homecontent import HomeContent


pygtk.require("2.0")


class MainView(object):

    _home_content = None
    _examination_content = None
    _addpatient_content = None
    _current_content = None
    _container = None

    def __init__(self):

        builder = gtk.Builder()
        builder.add_from_file("views/gtkbuilder/libreosteo-gui.glade")
        builder.connect_signals(self)
        self._container = builder.get_object("hpanedLayoutContainer")
        ## Init and attach home content
        self._home_content = HomeContent(self._container)
        self._current_content = self._home_content

        self._addpatient_content = AddPatientContent()

        ## show window
        self.windowMain = builder.get_object("windowMain")
        self.windowMain.show()

    def on_button_new_patient_clicked(self, sender):
        if self._current_content != self._addpatient_content:
            self._container.remove(self._current_content.get_maincontent())
            self._current_content = self._addpatient_content
            self._container.add(self._current_content.get_maincontent())

    def on_button_home_clicked(self, sender):
        if self._current_content != self._home_content:
            self._container.remove(self._current_content.get_maincontent())
            self._current_content = self._home_content
            self._container.add(self._current_content.get_maincontent())

    def on_windowMain_destroy(self, widget, data=None):
        gtk.main_quit()

