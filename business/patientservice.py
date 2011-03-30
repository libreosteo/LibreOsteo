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

class RegularDoctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key = True)
    family_name = Column(Unicode, nullable = False)
    firstname = Column(Unicode, nullable = False)
    phone = Column(Unicode)
    city = Column(Unicode)

    def __init__(self, family_name = None, firstname = None, phone = None,
                 city = None):
        self.family_name = family_name
        self.firstname = firstname
        self.phone = phone
        self.city = city

    def __repr__(self):
        return u"<Doctor('%s','%s', '%s')" % (self.family_name, self.firstname, self.city)


class Children(Base):
    __tablename__ = 'children'

    id = Column(Integer, primary_key = True)
    family_name = Column(Unicode, nullable = True)
    firstname = Column(Unicode, nullable = False)
    birthday_date = Column(Date)
    parent_id = Column(Integer, ForeignKey('patients.id'))
    

    def __init__(self, family_name = None, firstname = None, birthday_date = None):
        self.family_name = family_name
        self.firstname = firstname
        self.birthday_date = birthday_date
        

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key = True)
    family_name = Column(Unicode, nullable = False)
    original_name = Column(Unicode, nullable = True)
    firstname = Column(Unicode)
    birth_date = Column(Date)
    address_street = Column(Unicode)
    address_complement = Column(Unicode)
    address_zipcode = Column(Integer)
    address_city = Column(Unicode)
    phone = Column(Unicode)
    mobile_phone = Column(Unicode, nullable = True)
    family_situation = Column(Integer)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship("RegularDoctor")
    children = relationship("Children")

    def __init__(self, family_name = None, firstname = None, birth_date = None,
                 address_street = None, address_complement = None, address_zipcode = None, address_city = None,
                 phone = None, family_situation = None, original_name = None, mobile_phone = None):
        self.family_name = family_name
        self.original_name = original_name
        self.firstname = firstname
        self.birth_date = birth_date
        self.address_street = address_street
        self.address_complement = address_complement
        self.address_zipcode = address_zipcode
        self.address_city = address_city
        self.phone = phone
        self.mobile_phone = mobile_phone
        self.family_situation = family_situation

    def __repr__(self):
        return u"<Patient('%s','%s')" % (self.family_name, self.firstname)
    
