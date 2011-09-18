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

import unittest
import sys
sys.path.append("..")
from businessmodel import Base
from examinationmodel import Examination
from patientmodel import Patient, RegularDoctor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date


class TestExaminationService(unittest.TestCase):

    def setUp(self):
        self.patient1_values = [u'Dupond', u'Jean', date(1980, 3, 12),
        u'123 avenue Champ Vert', u'', u'92000', u'TOINTOIN', u'0102030405', 1]
        self.doctor1_values = [u'Alatete', u'Gémal', u'0102030405',
        u'TOINTOIN']
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        patient = Patient()
        patient.family_name = self.patient1_values[0]
        patient.firstname = self.patient1_values[1]
        patient.birth_date = self.patient1_values[2]
        patient.address_street = self.patient1_values[3]
        patient.address_complement = self.patient1_values[4]
        patient.address_zipcode = self.patient1_values[5]
        patient.address_city = self.patient1_values[6]
        patient.phone = self.patient1_values[7]
        patient.family_situation = self.patient1_values[8]

        doctor = RegularDoctor()
        doctor.family_name = self.doctor1_values[0]
        doctor.firstname = self.doctor1_values[1]
        doctor.phone = self.doctor1_values[2]
        doctor.city = self.doctor1_values[3]

        patient.doctor = doctor

        self.patient = patient

        self.session.add(patient)
        self.session.commit()

    def test_defineExamination(self):
        examination = Examination()
        examination.date = date.today()
        examination.patient = self.patient

        self.session.add(examination)
        self.session.commit()

        self.assertTrue(examination.id)
        self.assertEquals(self.doctor1_values[0],
        examination.patient.doctor.family_name)


if __name__ == '__main__':
    unittest.main()
