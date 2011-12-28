# -*- coding: utf-8 -*-


import pygtk
import gtk
import datetime
import time
import gobject


format_date = "%d/%m/%Y"

class CalendarEntry (gtk.HBox):
    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))
    }

    def __init__(self, entryLabel, displayAge=False, parent=None):
        gtk.HBox.__init__(self, False, 0)
        self.calendar = gtk.Calendar()
        self.entry = gtk.Entry()
        self.entry.set_editable(False)
        self.button = gtk.Button(label="...")
        self.ageLabel = gtk.Label(entryLabel)
        self.ageEntry = gtk.Entry()
        self.cwindow = gtk.Window(gtk.WINDOW_POPUP)
        self.display = False
        self.currentDate = None

        self.cwindow.set_position(gtk.WIN_POS_MOUSE)
        self.cwindow.set_decorated(False)
        self.cwindow.set_modal(False)
        self.cwindow.add(self.calendar)
        self.calendar.show()
        self.cwindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)

        self.ageEntry.set_editable(False)
        self.ageEntry.set_width_chars(3)
        self.ageEntry.set_property("can-focus", False)
        self.ageEntry.set_alignment(0.5)

        self.entry.set_width_chars(10)

        self.pack_start(self.entry, True, True, 4)
        self.pack_start(self.button, False, False, 4)

        self.__connect_signals()
        #self.update_entry()
        self.set_display_age(displayAge)

    def __connect_signals(self):
        self.day_selected_handle = self.calendar.connect("day-selected", self.update_entry)
        self.day_selected_double_handle = self.calendar.connect("day-selected-double-click", self.hide_widget)
        self.clicked_handle = self.button.connect("clicked", self.show_widget)
        self.activate = self.entry.connect("activate", self.update_calendar)
        self.focus_out = self.entry.connect("focus-out-event", self.focus_out_event)

    def __block_signals(self):
        self.calendar.handler_block(self.day_selected_handle)
        self.calendar.handler_block(self.day_selected_double_handle)
        self.button.handler_block(self.clicked_handle)
        self.entry.handler_block(self.activate)
        self.entry.handler_block(self.focus_out)

    def __unblock_signals(self):
        self.calendar.handler_unblock(self.day_selected_handle)
        self.calendar.handler_unblock(self.day_selected_double_handle)
        self.button.handler_unblock(self.clicked_handle)
        self.entry.handler_unblock(self.activate)
        self.entry.handler_unblock(self.focus_out)

    def calculateAge(self, born):
        """Calculate the age of a user."""
        today = datetime.date.today()
        birthday = datetime.date(today.year, born.month, born.day)
        try:
            birthday = datetime.date(today.year, born.month, born.day)
        except ValueError:
            # Raised when person was born on 29 February and the current year is not a leap year.
            birthday = datetime.date(today.year, born.month, born.day - 1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_text(self):
        return self.entry.get_text()

    def set_text(self, text):
        self.entry.set_text(text)

    def update_age_display(self, d=None):
        self.ageEntry.set_text(str(self.calculateAge(self.get_date())))

    def set_display_age(self, display):
        if display and not self.display:
            self.hide_all()
            self.pack_start(self.ageLabel, False, True, 4)
            self.pack_start(self.ageEntry, False, False, 4)
            self.show_all()
        elif not display and self.display:
            self.hide_all()
            self.remove(self.ageLabel)
            self.remove(self.ageEntry)
            self.show_all()
        self.display = display

    def set_date(self, date):
        if not date:
            date = datetime.date.fromtimestamp(time.time())
        self.currentDate = date
        self.__block_signals()
        self.calendar.select_day(1)
        self.calendar.select_month(self.currentDate.month-1, self.currentDate.year)
        self.calendar.select_day(self.currentDate.day)
        self.__unblock_signals()
        self.update_entry()

    def get_date(self):
        return self.currentDate

    def hide_widget(self, *args):
        self.cwindow.hide_all()

    def show_widget(self, *args):
        self.cwindow.show_all()
        self.entry.grab_focus()
    
    def update_entry(self, *args):
        year, month, day = self.calendar.get_date()
        month = month + 1
        self.currentDate = datetime.date(year, month, day)
        text = self.currentDate.strftime(format_date)
        self.entry.set_text(text)
        self.update_age_display(self.currentDate)
        self.emit("changed", self.currentDate)

    def update_calendar(self, *args):
        try:
            dt = datetime.datetime.strptime(self.entry.get_text(), format_date)
            self.set_date(dt)
        except:
                #print "CalendarEntry.update_calendar: Error parsing date, setting it as today..."
                #dt = datetime.date.fromtimestamp(time.time())
            pass

        self.hide_widget()

    def focus_out_event(self, widget, event):
        self.update_calendar()

