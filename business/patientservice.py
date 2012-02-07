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
from business.businessservice import BusinessService
from business.patientmodel import Patient, Children
import unicodedata


def match_patient(completion, key, iter, column):
	model = completion.get_model()
	text = model.get_value(iter, column)
	if text:
		return simplify_text(key) in simplify_text(text.lower())
	return None


def simplify_text(text):
	if isinstance(text, str):
		text = unicode(text, "utf8", "replace")
		text = unicodedata.normalize('NFD', text)
		return text.encode('ascii', 'ignore')
	return text


class PatientService(BusinessService):

	EVENT_ADD_PATIENT = "add_patient_event"
	EVENT_EDIT_PATIENT = "edit_patient_event"
	EVENT_ADD_CHILD = "add_child_event"
	EVENT_DELETE_CHILD = "delete_child_event"
	EVENT_EDIT_CHILD = "edit_child_event"
	
	def __init__(self, datalayer=None):
		BusinessService.__init__(self)
		if datalayer is not None:
			self._datalayer = datalayer

	def get_patient_list(self):
		return self.get_datalayer().query(Patient).all()

	def get(self, id):
		return self.get_datalayer().query(Patient).filter(
		        Patient.id == id).first()

	def save(self, patient):
		self.get_datalayer().add(patient)
		try:
			self.get_datalayer().commit()
		except:
			self.get_datalayer().rollback()
		self.emit(PatientService.EVENT_ADD_PATIENT, patient)

	def update(self, patient):
		self.get_datalayer().merge(patient)
		try:
			self.get_datalayer().commit()
		except:
			self.get_datalayer().rollback()
		self.emit(PatientService.EVENT_EDIT_PATIENT, patient)

	def get_children_list(self, patient):
		return self.get_datalayer().query(Children).filter(Children.parent_id == patient.id).all()
	
	def save_child(self, child):
		self.get_datalayer().add(child)
		try:
			self.get_datalayer().commit()
			self.get_logger().debug("save child on this patient = %s"  % child.parent)
		except:
			self.get_datalayer().rollback()
		self.emit(PatientService.EVENT_ADD_CHILD, child.parent)
	
	def delete_child(self, child):
		self.get_datalayer().delete(child)
		try:
			self.get_datalayer().commit()
		except:
			self.get_datalayer().rollback()
		self.emit(PatientService.EVENT_DELETE_CHILD, child.parent)

	
	def get_child(self, child_id):
		return self.get_datalayer().query(Children).filter(Children.id == child_id).first()