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
import views
from views.contentview import ContentBuilder
from business import helperservice
from business.patientmodel import Patient, Smoker, Children
from business.helperservice import get_services
from views.datepicker import CalendarEntry
import views.datepicker as datepicker
from views.ValidatedEntry import *
from views.addchildcontent import AddChildContent

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
        self.birthdate_entry = CalendarEntry("Âge", False)
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
        
        self._children = []
        self._populate_liststore()

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
        patient.smoker = (self._maincontent.get_object("label_smoker_value").get_text() == Smoker().get_text(True))
        start, end = self._maincontent.get_object("textbuffer_important_info").get_bounds()
        patient.important_info = self._maincontent.get_object("textbuffer_important_info").get_slice(start, end, False)
        start, end = self._maincontent.get_object("textbuffer_ante_chir").get_bounds()
        patient.surgical_history = self._maincontent.get_object("textbuffer_ante_chir").get_slice(start, end, False)
        start, end = self._maincontent.get_object("textbuffer_ante_medic").get_bounds()
        patient.medical_history = self._maincontent.get_object("textbuffer_ante_medic").get_slice(start, end, False)
        start, end = self._maincontent.get_object("textbuffer_ante_familial").get_bounds()
        patient.family_history = self._maincontent.get_object("textbuffer_ante_familial").get_slice(start, end, False)        
        start, end = self._maincontent.get_object("textbuffer_ante_trauma").get_bounds()
        patient.trauma_history = self._maincontent.get_object("textbuffer_ante_trauma").get_slice(start, end, False)        
        get_services().get_patient_service().save(patient)
        
        # Add child if exists
        for child in self._children:
            child.parent_id = patient.id
            get_services().get_patient_service().save(child)
            
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
        self._maincontent.get_object("label_smoker_value").set_text(Smoker().get_text(False))
        self._maincontent.get_object("textbuffer_important_info").set_text('')
        self._maincontent.get_object("textbuffer_ante_chir").set_text('')
        self._maincontent.get_object("textbuffer_ante_medic").set_text('')
        self._maincontent.get_object("textbuffer_ante_familial").set_text('')
        self._maincontent.get_object("textbuffer_ante_trauma").set_text('')
        self._children = []
        self._populate_liststore()

    def on_label_smoker_value_button_press_event(self, sender, event):
        label_smoker = self._maincontent.get_object("label_smoker_value")
        if label_smoker.get_text() == Smoker().get_text(True):
            label_smoker.set_text(Smoker().get_text(False))
        else :
            label_smoker.set_text(Smoker().get_text(True))

    def on_treeview_children_cursor_changed(self, sender):
        # When selection change on treeview for children.
        self._update_button_delete_child()
    
    def _update_button_delete_child(self):
        # Update button to delete
        (tree_model, tree_iter) = self._maincontent.get_object("treeview_children").get_selection().get_selected()
        if tree_iter is not None:
            child_index = tree_model[tree_iter][2]
            child = self._children[child_index]
            if child is not None:
                self._maincontent.get_object("button_children_delete").set_sensitive(True)
            else:
                self._maincontent.get_object("button_children_delete").set_sensitive(False)        
        else:
            self._maincontent.get_object("button_children_delete").set_sensitive(False)
    
    def on_button_children_delete_clicked(self, sender):
        (tree_model, tree_iter) = self._maincontent.get_object("treeview_children").get_selection().get_selected()
        child_index = tree_model[tree_iter][2]
        child = self._children[child_index]
        self._children.remove(child)
        self._populate_liststore()

    def on_button_children_add_clicked(self, sender):
        # TODO show dialog to edit child
        self._dialog_add = gtk.Dialog("Ajouter", views.mainview.main_window, gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self._widget_add_child = AddChildContent(self._maincontent.get_object("entry_name").get_text())
        self._dialog_add.vbox.pack_start(self._widget_add_child.get_maincontent())
        self._widget_add_child.get_maincontent().show()
        self._dialog_add.connect("response", self.cb_add_child)
        self._dialog_add.show_all()
    
    def cb_add_child(self, sender, response_id):
        if response_id == gtk.RESPONSE_ACCEPT:
            self._children.append(self._widget_add_child.retrieve_child())
        self._populate_liststore()
        self._dialog_add.destroy()        
    
    def _populate_liststore(self):
        liststore = self._maincontent.get_object("liststore_children")
        liststore.clear()
        for child in self._children:
            liststore.append([ child.family_name.upper()+ " "+child.firstname, helperservice.format_age(child.birthday_date), self._children.index(child)])
        self._update_button_delete_child()