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
from business.patientmodel import Patient
from business.helperservice import get_services
from views.datepicker import CalendarEntry
import views.datepicker as datepicker
from views.ValidatedEntry import *

__version__ = "$Rev$"


class AddPatientContent(object):

    _gladefile = "views/gtkbuilder/libreosteo-add_patient.glade"
    _maincontent_name = "maincontent"
    _maincontent = None

    def __init__(self, parent=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        hbox = self._maincontent.get_object("hboxdatepicker")
        self.birthdate_entry = CalendarEntry("Âge", True)
        hbox.pack_end(self.birthdate_entry)
        hbox.show_all()

        hbox = self._maincontent.get_object("hbox_phone")
        self.phone_entry = ValidatedEntry(v_phone)
        hbox.pack_end(self.phone_entry)
        hbox.show_all()
        hbox = self._maincontent.get_object("hbox_mobile_phone")
        self.mobile_entry = ValidatedEntry(v_phone)
        hbox.pack_end(self.mobile_entry)
        hbox.show_all()

        hbox = self._maincontent.get_object("hbox_zipcode")
        self.zipcode_entry = ValidatedEntry(v_zipcode)
        hbox.pack_end(self.zipcode_entry)
        hbox.show_all()

        self._maincontent.connect_signals(self)

    def get_maincontent(self):
        return self._maincontent.get_object(self._maincontent_name)

    def on_button_add_clicked(self, sender):
        #Get all data from form and populate patient model
        family_name = self._maincontent.get_object("entry_name").get_text()
        firstname = self._maincontent.get_object("entry_firstname").get_text()
        birth_date = helperservice.get_date(
            self.birthdate_entry.get_text(), datepicker.format_date)
        address_street = self._maincontent.get_object(
            "entry_street").get_text()
        address_complement = self._maincontent.get_object(
            "entry_complement").get_text()
        address_zipcode = self.zipcode_entry.get_text()
        address_city = self._maincontent.get_object("entry_city").get_text()
        phone = self.phone_entry.get_text()
        model_family_situation = self._maincontent.get_object("combobox_family_situation").get_model()
        print str(model_family_situation)
        family_situation_iter = self._maincontent.get_object(
            "combobox_family_situation").get_active_iter()
        if family_situation_iter:
            family_situation = model_family_situation[family_situation_iter][1]
        else:
            family_situation = None
        original_name = None
        mobile_phone = self.mobile_entry.get_text()
        patient = Patient(family_name, firstname, birth_date,
                 address_street, address_complement,
                 address_zipcode, address_city,
                 phone, family_situation, original_name,
                 mobile_phone)
        get_services().get_patient_service().save(patient)
        self.reset_form()

    def reset_form(self):
        self._maincontent.get_object("entry_name").set_text('')
        self._maincontent.get_object("entry_firstname").set_text('')
        self.birthdate_entry.set_text('')
        self._maincontent.get_object(
            "entry_street").set_text('')
        self._maincontent.get_object(
            "entry_complement").set_text('')
        self.zipcode_entry.set_text('')
        self._maincontent.get_object("entry_city").set_text('')
        self.mobile_entry.set_text('')
        self.phone_entry.set_text('')
        self._maincontent.get_object(
            "combobox_family_situation").set_active(-1)
        original_name = None
        self._maincontent.get_object(
            "entry_mobile_phone").set_text('')

