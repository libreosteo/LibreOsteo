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
from business.patientmodel import Patient, Smoker
from business.helperservice import get_services
from views.datepicker import CalendarEntry
import views.datepicker as datepicker
from views.ValidatedEntry import *
from views.addchildcontent import AddChildContent
from views.modifychildcontent import ModifyChildContent

__version__ = "$Rev$"


class ModifyPatientContent(object):

	_gladefile = "views/gtkbuilder/libreosteo-edit_patient.glade"
	_maincontent_name = "maincontent"
	_maincontent = None

	def __init__(self, patient=None, parent=None):
		content_builder = ContentBuilder()
		content_builder.gladefile = self._gladefile
		self._maincontent = content_builder.view
		hbox = self._maincontent.get_object("hboxdatepicker")
		self.birthdate_entry = CalendarEntry("Âge", False, parent)
		self.birthdate_entry.cwindow.set_transient_for(parent)
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
		self._patient = patient
		self._fill()
		get_services().patient_service.add_listener(self, get_services().patient_service.EVENT_EDIT_PATIENT)
		get_services().patient_service.add_listener(self, get_services().patient_service.EVENT_ADD_CHILD)
		get_services().patient_service.add_listener(self, get_services().patient_service.EVENT_DELETE_CHILD)
		get_services().patient_service.add_listener(self, get_services().patient_service.EVENT_EDIT_CHILD)

	def get_maincontent(self):
		return self._maincontent.get_object(self._maincontent_name)

	def _fill(self):
		self.reset_form()
		if self._patient.family_name:
			self._maincontent.get_object("entry_name").set_text(self._patient.family_name)
		if self._patient.firstname:
			self._maincontent.get_object("entry_firstname").set_text(self._patient.firstname)
		if self._patient.birth_date:
			self.birthdate_entry.set_date(self._patient.birth_date)
		if self._patient.address_street :
			self._maincontent.get_object(
			        "entry_street").set_text(self._patient.address_street)
		if self._patient.address_complement:
			self._maincontent.get_object(
			        "entry_complement").set_text(self._patient.address_complement)
		if self._patient.address_zipcode:
			self.zipcode_entry.set_text(self._patient.address_zipcode)
		if self._patient.address_city:
			self._maincontent.get_object("entry_city").set_text(self._patient.address_city)
		if self._patient.mobile_phone:
			self.mobile_entry.set_text(self._patient.mobile_phone)
		if self._patient.phone:
			self.phone_entry.set_text(self._patient.phone)
		if not self._patient.family_situation is None:
			self._maincontent.get_object(
			        "combobox_family_situation").set_active(self._patient.family_situation)
		self._maincontent.get_object("label_smoker_value").set_text(Smoker().get_text(self._patient.smoker))

		if self._patient.important_info:
			self._maincontent.get_object("textbuffer_important_info").set_text(self._patient.important_info)
		if self._patient.surgical_history:
			self._maincontent.get_object("textbuffer_ante_chir").set_text(self._patient.surgical_history)
		if self._patient.medical_history:
			self._maincontent.get_object("textbuffer_ante_medic").set_text(self._patient.medical_history)
		if self._patient.family_history:
			self._maincontent.get_object("textbuffer_ante_familial").set_text(self._patient.family_history)
		if self._patient.trauma_history:
			self._maincontent.get_object("textbuffer_ante_trauma").set_text(self._patient.trauma_history)
		self._fill_children_list()   
			
		original_name = None
		self._update_button_child()

	def _fill_children_list(self):
		liststore = self._maincontent.get_object("liststore_children")
		liststore.clear()
		list_children = get_services().patient_service.get_children_list(self._patient)
		for child in list_children :
			liststore.append([ child.family_name.upper()+ " "+child.firstname, helperservice.format_age(child.birthday_date), child.id])
		self._update_button_child()

	def on_treeview_children_cursor_changed(self, sender):
		# When selection change on treeview for children.
		self._update_button_child()

	def _update_button_child(self):
		selection = self._maincontent.get_object("treeview_children").get_selection()
		if selection is not None :
			(tree_model, tree_iter) = selection.get_selected()
			if tree_iter is not None:
				child_index = tree_model[tree_iter][2]
				child = get_services().patient_service.get_child(child_index)
				if child is not None:
					# Update button to delete
					self._maincontent.get_object("button_delete_child").set_sensitive(True)
					self._maincontent.get_object("button_modify_child").set_sensitive(True)
				else:
					self._maincontent.get_object("button_delete_child").set_sensitive(False)
					self._maincontent.get_object("button_modify_child").set_sensitive(False)
			else:
				self._maincontent.get_object("button_delete_child").set_sensitive(False)
				self._maincontent.get_object("button_modify_child").set_sensitive(False)

	def on_button_delete_child_clicked(self, sender):
		(tree_model, tree_iter) = self._maincontent.get_object("treeview_children").get_selection().get_selected()
		if tree_iter is not None:
			child_index = tree_model[tree_iter][2]
			child = get_services().patient_service.get_child(child_index)
			get_services().patient_service.delete_child(child)
			self._maincontent.get_object("treeview_children").get_selection().unselect_iter(tree_iter)

	def on_button_modify_child_clicked(self, sender):
		(tree_model, tree_iter) = self._maincontent.get_object("treeview_children").get_selection().get_selected()
		if tree_iter is not None:
			child_index = tree_model[tree_iter][2]
			child = get_services().patient_service.get_child(child_index)
			self._dialog_modify = gtk.Dialog("Modifier", views.mainview.main_window, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			self._widget_modify_child = ModifyChildContent(child)
			self._dialog_modify.vbox.pack_start(self._widget_modify_child.get_maincontent())
			self._dialog_modify.connect("response", self.cb_modify_child)
			self._dialog_modify.show_all()

	def on_button_add_child_clicked(self, sender):
		self._dialog_add = gtk.Dialog("Ajouter", views.mainview.main_window, gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
				      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		self._widget_add_child = AddChildContent(self._maincontent.get_object("entry_name").get_text())
		self._dialog_add.vbox.pack_start(self._widget_add_child.get_maincontent())
		self._widget_add_child.get_maincontent().show()
		self._dialog_add.connect("response", self.cb_add_child)
		self._dialog_add.show_all()	
		
	def cb_add_child(self, sender, response_id):
		if response_id == gtk.RESPONSE_ACCEPT:
			child = self._widget_add_child.retrieve_child()
			child.parent_id = self._patient.id
			child.parent = self._patient
			get_services().get_patient_service().save_child(child)
		self._fill_children_list()
		self._dialog_add.destroy()
		
	def cb_modify_child(self, sender, response_id):
		if response_id == gtk.RESPONSE_ACCEPT:
			child = self._widget_modify_child.retrieve_child()
			get_services().get_patient_service().save_child(child)
		self._fill_children_list()
		self._dialog_modify.destroy()

	def modify(self):
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
		family_situation_iter = self._maincontent.get_object(
		        "combobox_family_situation").get_active_iter()
		if family_situation_iter:
			family_situation = model_family_situation[family_situation_iter][1]
		else:
			family_situation = None
		original_name = None
		mobile_phone = self.mobile_entry.get_text()
		
		self._patient.family_name = family_name
		self._patient.firstname = firstname
		self._patient.birth_date = birth_date
		self._patient.address_street = address_street
		self._patient.address_complement = address_complement
		self._patient.address_zipcode = address_zipcode
		self._patient.address_city = address_city
		self._patient.phone = phone
		self._patient.mobile_phone = mobile_phone
		self._patient.family_situation = family_situation
		
		self._patient.smoker = (self._maincontent.get_object("label_smoker_value").get_text() == Smoker().get_text(True))
		start, end = self._maincontent.get_object("textbuffer_important_info").get_bounds()
		self._patient.important_info = self._maincontent.get_object("textbuffer_important_info").get_slice(start, end, False)
		start, end = self._maincontent.get_object("textbuffer_ante_chir").get_bounds()
		self._patient.surgical_history = self._maincontent.get_object("textbuffer_ante_chir").get_slice(start, end, False)
		start, end = self._maincontent.get_object("textbuffer_ante_medic").get_bounds()
		self._patient.medical_history = self._maincontent.get_object("textbuffer_ante_medic").get_slice(start, end, False)
		start, end = self._maincontent.get_object("textbuffer_ante_familial").get_bounds()
		self._patient.family_history = self._maincontent.get_object("textbuffer_ante_familial").get_slice(start, end, False)
		start, end = self._maincontent.get_object("textbuffer_ante_trauma").get_bounds()
		self._patient.trauma_history = self._maincontent.get_object("textbuffer_ante_trauma").get_slice(start, end, False)
		
		get_services().get_patient_service().update(self._patient)

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
		self._maincontent.get_object("label_smoker_value").set_text(Smoker().get_text(False))
		self._maincontent.get_object("textbuffer_important_info").set_text('')
		self._maincontent.get_object("label_smoker_value").set_text(Smoker().get_text(False))
		self._maincontent.get_object("textbuffer_important_info").set_text('')
		self._maincontent.get_object("textbuffer_ante_chir").set_text('')
		self._maincontent.get_object("textbuffer_ante_medic").set_text('')
		self._maincontent.get_object("textbuffer_ante_familial").set_text('')
		self._maincontent.get_object("textbuffer_ante_trauma").set_text('')            
		original_name = None

	def on_label_smoker_value_button_press_event(self, sender, event):
		label_smoker = self._maincontent.get_object("label_smoker_value")
		if label_smoker.get_text() == Smoker().get_text(True):
			label_smoker.set_text(Smoker().get_text(False))
		else :
			label_smoker.set_text(Smoker().get_text(True))

	def notify(self, event, *args):
		if event == get_services().patient_service.EVENT_EDIT_PATIENT:
			((patient,),) =  args
			if self._patient.id == patient.id:
				self._patient = patient
				self._patient.children = get_services().patient_service.get_children_list(patient)
				self._fill()
		if event == get_services().patient_service.EVENT_ADD_CHILD or event == get_services().patient_service.EVENT_DELETE_CHILD or event == get_services().patient_service.EVENT_EDIT_CHILD:
			((patient,),) = args
			if self._patient.id == patient.id:
				self._patient = patient
				self._patient.children = get_services().patient_service.get_children_list(patient)
				self._fill_children_list()
		