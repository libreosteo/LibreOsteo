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
from core.configuration import Configuration
from optparse import OptionParser
from core.datalayer import DatasourceFactory
from views import mainview
from views.mainview import MainView
from business import businessservice

pygtk.require("2.0")

configuration_file_path = "~/.libreosteo/libreosteo.conf"


def init_option_parser():
    parser = OptionParser()
    parser.add_option("-c", action="store", dest="config_file",
                  help="path to config file",
                  default=configuration_file_path)
    return parser

if __name__ == "__main__":
    parser = init_option_parser()
    (options, args) = parser.parse_args()
    configuration_object = Configuration(options.config_file)
    datasource_factory = DatasourceFactory(configuration_object)
    businessservice.internal_datalayer = datasource_factory.get_datasource()
    app = MainView()
    mainview.main_window = app.windowMain
    gtk.main()
