#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
from django.utils.dateparse import parse_datetime
from robot.api import logger
import sqlite3
import datetime

FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def format_longdate(date):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    return '%s %s' % (date.day, date.strftime('%B %Y'))


def convert_django_timezone_date(date_str):
    return parse_datetime(date_str)


def should_be_equal_as_date_only(date1, date2):
    if not (date1.day == date2.day and date1.month == date2.month
            and date1.year == date2.year):
        raise AssertionError("%s and %s are not date equal" % (date1, date2))


def get_date_invoice(invoice_number):
    logger.info("Retrieve the current date on invoice number = %s " %
                invoice_number)
    con = sqlite3.connect("data/db.sqlite3",
                          detect_types=sqlite3.PARSE_DECLTYPES)

    cur = con.cursor()
    cur.execute("SELECT date from libreosteoweb_invoice where number = ? ",
                (invoice_number, ))
    d = cur.fetchone()
    return datetime.datetime.strptime(d[0], FORMAT)


def change_date_invoice(invoice_number, date):
    con = sqlite3.connect("data/db.sqlite3",
                          detect_types=sqlite3.PARSE_DECLTYPES)

    cur = con.cursor()
    cur.execute("UPDATE libreosteoweb_invoice set date = ? where number = ? ",
                (datetime.datetime.strftime(date, FORMAT), invoice_number))
    con.commit()


def change_date_examination(examination, date):
    con = sqlite3.connect("data/db.sqlite3",
                          detect_types=sqlite3.PARSE_DECLTYPES)

    cur = con.cursor()
    cur.execute("UPDATE libreosteoweb_examination set date = ? where id = ? ",
                (datetime.datetime.strftime(date, FORMAT), examination))
    con.commit()
