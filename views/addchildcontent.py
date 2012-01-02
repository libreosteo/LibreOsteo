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
from views.datepicker import CalendarEntry
import views.datepicker as datepicker
from business.patientmodel import Children

__version__ = "$Rev$"


class AddChildContent(object):

    _gladefile = "views/gtkbuilder/libreosteo-add_child.glade"
    _maincontent_name = "maincontent"
    _maincontent = None

    def __init__(self, default_family_name=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        hbox = self._maincontent.get_object("hbox_birth_date")
        self.birthdate_entry = CalendarEntry("Âge", False)
        hbox.pack_end(self.birthdate_entry)
        hbox.show_all()
        
        self._maincontent.get_object("entry_family_name").set_text(default_family_name)
    
    def retrieve_child(self):
        family_name = self._maincontent.get_object("entry_family_name").get_text()
        first_name = self._maincontent.get_object("entry_firstname").get_text()
        birth_date = helperservice.get_date(
            self.birthdate_entry.get_text(), datepicker.format_date)
        return Children(family_name=family_name, firstname=first_name, birthday_date=birth_date)
    
    def get_maincontent(self):
        return self._maincontent.get_object(self._maincontent_name)    