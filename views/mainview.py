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
from views.examinationcontent import ExaminationContent
from business.helperservice import get_services


pygtk.require("2.0")

main_window = None

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
        
        self._ui_builder = builder

        self._addpatient_content = AddPatientContent()
        self._examination_content = ExaminationContent()
        
        self.examination_service = get_services().get_examination_service()
        self.examination_service.add_listener(self, self.examination_service.EVENT_EXAMINATION_READY)
        self.examination_service.add_listener(self, self.examination_service.EVENT_EXAMINATION_IDLE)
        
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
    
    def on_button_examination_clicked(self, sender):
        if self._current_content != self._examination_content:
            self._container.remove(self._current_content.get_maincontent())
            self._current_content = self._examination_content
            self._container.add(self._current_content.get_maincontent())
            self._examination_content.update()

    def on_windowMain_destroy(self, widget, data=None):
        gtk.main_quit()
        
    def notify(self, event, *args):
        if event == self.examination_service.EVENT_EXAMINATION_IDLE:
            self._ui_builder.get_object("button_examination").set_sensitive(False)
        if event == self.examination_service.EVENT_EXAMINATION_READY:
            self._ui_builder.get_object("button_examination").set_sensitive(True)

