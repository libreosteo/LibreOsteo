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
from business.patientservice import PatientService


pygtk.require("2.0")


class ContentBuilder(object):

    def __init__(self):
        self._builder = gtk.Builder()
        self._gladefile = None

    def get_gladefile(self):
        return self._gladefile

    def set_gladefile(self, gladefile):
        self._gladefile = gladefile

    gladefile = property(get_gladefile, set_gladefile)

    def get_view(self):
        if self.gladefile is not None:
            self._builder.add_from_file(self.gladefile)
        return self._builder

    view = property(get_view)

    def attach(self, parent_view, content_name):
        content_view = self._builder.get_object(content_name)
        content_view.reparent(parent_view)


class HomeContent(object):

    _gladefile = "views/gtkbuilder/libreosteo-home.glade"
    _maincontent_name = "maincontent"
    _maincontent = None
    _liststore = None
    _entry_search = None
    _tabbed_panel = None

    def __init__(self, parent=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        self._maincontent.connect_signals(self)
        self._init_tabbed_panel()
        self._tabbed_panel.set_current_page(1)
        self._init_completer()
        if parent is not None:
            content_builder.attach(parent, self._maincontent_name)

    def _init_tabbed_panel(self):
        if self._tabbed_panel is None:
            self._tabbed_panel = self._maincontent.get_object("tabbedpanel")
        home_searcher = self._maincontent.get_object("vboxHomeSearcher")
        self._tabbed_panel.insert_page(home_searcher, gtk.Label("Rechercher"))

    def _init_completer(self):
        patient_completion = self._maincontent.get_object("completion_patient")
        self._liststore = gtk.ListStore(str, str)
        for patient in PatientService().get_patient_list():
            print "add patient " + patient.family_name
            self._liststore.append([patient.family_name, patient.firstname])
        patient_completion.set_model(self._liststore)
        self._entry_search = self._maincontent.get_object("entry_search")
        self._entry_search.set_completion(patient_completion)
        patient_completion.set_text_column(0)
        patient_completion.connect('match-selected', self.match_cb)

    def match_cb(self, completion, model, iter):
        print model[iter][0], 'was selected'
        print "curent page = " + str(self._tabbed_panel.get_current_page())
        print "number of page = " + str(self._tabbed_panel.get_n_pages())
        return

    def create_tab(self, title, tabbed_content):
        if tabbed_content is None:
            return
        hbox = gtk.HBox(False, 0)
        label = gtk.Label(title)
        hbox.pack_start(label)
        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE,
        gtk.ICON_SIZE_MENU)
        image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        hbox.pack_start(btn, False, False)

        #this reduces the size of the button
        style = gtk.RcStyle()
        style.xthickness = 0
        style.ythickness = 0
        btn.modify_style(style)

        hbox.show_all()

        #add the tab
        self._tabbed_panel.insert_page_menu(tabbed_content, hbox,
        gtk.Label(title))
        #connect the close button
        btn.connect('clicked', self.on_closetab_button_clicked, tabbed_content)
         # Need to refresh the widget --
        # This forces the widget to redraw itself.
        self._tabbed_panel.queue_draw_area(0, 0, -1, -1)

    def on_closetab_button_clicked(self, sender, widget):
        #get the page number of the tab we wanted to close
        pagenum = self._tabbed_panel.page_num(widget)
        #and close it
        self._tabbed_panel.remove_page(pagenum)

    def button_open_folder_clicked_cb(self, sender):
        self.create_tab("Test", FolderContent().get_widget())


class FolderContent(object):
    _gladefile = "views/gtkbuilder/libreosteo-folder_reader.glade"
    _maincontent_name = "maincontent"
    _maincontent = None

    def __init__(self, parent=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        self._maincontent.connect_signals(self)
        self._folder_content = self._maincontent.get_object(
            self._maincontent_name)

    def get_widget(self):
        return self._folder_content
