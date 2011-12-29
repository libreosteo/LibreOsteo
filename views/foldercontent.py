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
from business.helperservice import get_services
from business.patientmodel import Situation, Smoker


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
        self._tabbed_panel = None
        self._set_content()
        self._patient_service = get_services().get_patient_service()
        self._patient_service.add_listener(self, self._patient_service.EVENT_EDIT_PATIENT)
        
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
            if self._current_patient.smoker :
                self._maincontent.get_object(
                    "vbox_doctor").set_visible(True)
                self._maincontent.get_object("label_smoker_value").set_text(Smoker().get_text(self._current_patient.smoker))
            else :
                self._maincontent.get_object(
                    "vbox_doctor").set_visible(False)
        if len(self._current_patient.children) != 0:
            self.set_children()
        else:
            self._maincontent.get_object("vbox_children").set_visible(False)
        
        if self._current_patient.important_info :
            self._maincontent.get_object("textbuffer_important").set_text(self._current_patient.important_info)
        if self._current_patient.surgical_history:
            self._maincontent.get_object("textbuffer_ante_chir").set_text(self._current_patient.surgical_history)
        if self._current_patient.medical_history:
            self._maincontent.get_object("textbuffer_ante_medic").set_text(self._current_patient.medical_history)
        if self._current_patient.family_history:
            self._maincontent.get_object("textbuffer_ante_familial").set_text(self._current_patient.family_history)
        if self._current_patient.trauma_history:
            self._maincontent.get_object("textbuffer_ante_trauma").set_text(self._current_patient.trauma_history)
            

    def get_widget(self):
        if self._tabbed_panel is None:
            return self._folder_content
        else:
            return self._tabbed_panel

    def set_children(self):
        print self._current_patient.children

    def get_patient(self):
        return self._current_patient
    
    def notify(self, event, *args):
        if event == self._patient_service.EVENT_EDIT_PATIENT:
            ((patient,),) =  args
            if self._current_patient.id == patient.id:
                self._current_patient = patient
                self._set_content()
        