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
from business.patientmodel import Patient


class PatientService(BusinessService):

    def __init__(self, datalayer=None):
        BusinessService.__init__(self)
        if datalayer is not None:
            self._datalayer = datalayer

    def match_patient(completion, key, iter, column):
        print "passe ici"
        model = completion.get_model()
        print "Key = " + key
        return model[iter][COL_TEXT].startswith(self.get_text())
        text = model.get_value(iter, column)
        if text.startwith(key):
            return True
        return False

    def get_patient_list(self):
        return self.get_datalayer().query(Patient).all()

