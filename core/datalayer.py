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

from __future__ import absolute_import
from sqlalchemy import create_engine
from business.businessmodel import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.orm.session import Session


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)

    def __init__(self):
        Base.__init__(self)


class DatasourceFactory(object):

    _engine = None
    _sessionfactory = None

    def __init__(self, config_object):
        if config_object.datasource:
            dblink = config_object.datasource['dblink']
            if dblink is not None:
                self._engine = create_engine(dblink, echo=True)
            if self._is_empty():
                self._init_database()
        self._datasource = self._sessionfactory

    def _is_empty(self):
        self._sessionfactory = sessionmaker(bind=self._engine)
        session = self._sessionfactory()
        try:
            test_result = session.query(Test).first()
        except:
            return True
        finally:
            session.rollback()
        return test_result is None

    def _init_database(self):
        Base.metadata.create_all(self._engine)
        print "init_db"
        if self._sessionfactory is None:
            self._sessionfactory = sessionmaker(bind=self._engine)
        session = self._sessionfactory()
        session.add(Test())
        session.commit()

    def get_datasource(self):
        return self._datasource
