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

from business.businessservice import BusinessService
from business.examinationmodel import Examination

class ExaminationService(BusinessService):

	EVENT_EXAMINATION_READY = "examination_ready"
	EVENT_EXAMINATION_IDLE = "examination_idle"
	EVENT_ASK_EXAMINATION = "ask_examination"

	def __init__(self, datalayer=None):
		BusinessService.__init__(self)
		if datalayer is not None:
			self._datalayer = datalayer
		self._current_patient = None

	def get_status_text(self, status):
		if status == Examination.STATUS_CANCELED:
			return "Annulée"
		if status == Examination.STATUS_SOLD:
			return "Réglée"
		if status == Examination.STATUS_WAIT:
			return "En attente"
		return ""

	def set_current_patient(self, patient):
		self._current_patient = patient
		if patient != None :
			self.emit(self.EVENT_EXAMINATION_READY)
		else :
			self.emit(self.EVENT_EXAMINATION_IDLE)

	def get_current_patient(self):
		return self._current_patient

	def ask_for_examination(self):
		self.emit(self.EVENT_ASK_EXAMINATION)

	def save(self, examination):
		self.get_datalayer().add(examination)
		self.get_datalayer().commit()

	def request_for_examination(self, patient_id, date):
		return self.get_datalayer().query(Examination).filter(
		        Examination.patients_id == patient_id).filter(Examination.date == date).first()

	def get_examination_list(self, patient_id):
		return self.get_datalayer().query(Examination).filter(Examination.patients_id == patient_id).order_by(Examination.date).all()

	def get_examination(self, examination_id):
		return self.get_datalayer().query(Examination).filter(Examination.id == examination_id).first()