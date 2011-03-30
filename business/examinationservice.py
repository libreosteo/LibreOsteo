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

from businessmodel import Base
from sqlalchemy import Column, Unicode, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

class Examination(Base):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key = True)
    trauma_family = Column(Unicode, nullable = True)
    trauma_medical = Column(Unicode, nullable = True)
    trauma_surgical = Column(Unicode, nullable = True)
    medical_examination = Column(Unicode, nullable = True)
    tests = Column(Unicode)
    diagnosis = Column(Unicode)
    treatments = Column(Unicode)
    conclusion = Column(Unicode)
    date = Column(Date)
    facture_id = Column(Integer, ForeignKey('factures.id'))
    patients_id = Column(Integer, ForeignKey('patients.id'))
    facture = relationship("Facture")
    patient = relationship("Patient")

    def __init__(self,trauma_family = None, trauma_medical = None, trauma_surgical = None,
                 medical_examination = None, tests = None, diagnosis = None,
                 treatments = None, conclusion = None, date = None):
        self.trauma_family = trauma_family
        self.trauma_medical = trauma_medical
        self.trauma_surgical = trauma_surgical
        self.medical_examination = medical_examination
        self.tests = tests
        self.diagnosis = diagnosis
        self.treatments = treatments
        self.conclusion = conclusion
        self.date = date
        self.patient = None

    def __repr__(self):
        return u"<Examination('%s', '%s')" % (self.date, self.patient)


class Facture(Base):
    __tablename__ = "factures"

    id = Column(Integer, primary_key = True)
    date = Column(Date)
    
