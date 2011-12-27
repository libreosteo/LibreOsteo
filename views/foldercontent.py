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
from views.contentview import ContentBuilder
from business import helperservice
from business.patientmodel import Situation


class FolderContent(object):
    _gladefile = "views/gtkbuilder/libreosteo-folder_reader.glade"
    _maincontent_name = "maincontent"
    _maincontent = None
    _current_patient = None

    def __init__(self, patient=None, parent=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        self._maincontent.connect_signals(self)
        self._folder_content = self._maincontent.get_object(
            self._maincontent_name)
        self._current_patient = patient
        self._set_content()

    def _set_content(self):
        self._maincontent.get_object("label_name_value").set_text(
            self._current_patient.family_name.upper())
        self._maincontent.get_object("label_firstname_value").set_text(
            self._current_patient.firstname)
        self._maincontent.get_object("label_address_value").set_text(
            helperservice.format_address(self._current_patient))
        self._maincontent.get_object("label_age_value").set_text(
            helperservice.format_age(self._current_patient))
        if self._current_patient.phone is not None:
            self._maincontent.get_object("label_phone_value").set_text(
                self._current_patient.phone)
        else:
            self._maincontent.get_object("label_phone_value").set_text("")
        if self._current_patient.mobile_phone is not None:
            self._maincontent.get_object("label_phone_mobile_value").set_text(
                self._current_patient.mobile_phone)
        else:
            self._maincontent.get_object("label_phone_mobile_value").set_text(
                "")
        if self._current_patient.family_situation is not None:
            self._maincontent.get_object("label_family_status_value").set_text(
                Situation().get_text(self._current_patient.family_situation))
        else:
            self._maincontent.get_object("label_family_status_value").set_text(
                "")
        if self._current_patient.doctor is not None:
            self.set_doctor()
        else:
            self._maincontent.get_object(
                "vbox_doctor").set_visible(False)
        if len(self._current_patient.children) != 0:
            self.set_children()
        else:
            self._maincontent.get_object("vbox_children").set_visible(False)

    def get_widget(self):
        return self._folder_content

    def set_children(self):
        print "passe ici :o"
        print self._current_patient.children
