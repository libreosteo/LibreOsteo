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

import datetime


def format_address(patient):
    format_template = "{0[street]}"
    dico = dict(street=patient.address_street)
    if patient.address_street is not None:
        if patient.address_complement is not None:
            format_template += "\n{0[complement]}"
            dico['complement'] = patient.address_complement
        if patient.address_zipcode is not None:
            format_template += "\n{0[zipcode]}"
            dico['zipcode'] = patient.address_zipcode
        if patient.address_city is not None:
            if 'zipcode' in dico.keys():
                format_template += " "
            format_template += "{0[city]}"
            dico['city'] = patient.address_city.upper()
        return format_template.format(dico)
    return ""


def format_age(patient):
    if patient.birth_date is None:
        return ""
    delta = datetime.date.today() - patient.birth_date
    age_year = int(delta.days / 365.25)
    if age_year == 0:
        age_month = int(delta.days / 31.0)
        age_format = "%s mois" % (age_month)
    elif age_year < 3:
        age_year = int(delta.days / 365.25)
        age_month = int((delta.days - age_year * 365.25) / 31.0)
        year_unit = "an"
        if age_year > 1:
            year_unit += "s"
        age_format = "%s %s et %s mois" % (age_year, year_unit, age_month)
    else:
        age_format = "%s ans" % (age_year)
    return age_format


def get_date(string_date, format_date):
    if len(string_date) != 0:
        return datetime.datetime.strptime(string_date, format_date)
    return None


from business.patientservice import PatientService


def get_services():
    try:
        helper_service = HelperService()
    except HelperService, h:
        helper_service = h
    return helper_service


class HelperService:

    instance = None

    def __init__(self):
        if HelperService.instance:
            raise HelperService.instance
        HelperService.instance = self
        self.patient_service = PatientService()

    def get_patient_service(self):
        return self.patient_service
