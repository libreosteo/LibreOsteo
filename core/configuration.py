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


"""
This class parse a config file in INI format
access to configuration per section
for example :
    [section_main]
    value1 = val

access with :
>>> c = Configuration('configfile.cfg')
>>> c.section_main
['value1']
>>> c.section_main['value1']
val

"""

import ConfigParser
import os.path

home_libreosteo = os.path.expanduser("~/.libreosteo")
db_path_libreosteo = os.path.expanduser("~/.libreosteo/libreosteo.db")


def create_default_config_file(str_file):
    if not os.path.isdir(home_libreosteo):
        os.mkdir(home_libreosteo)
    fp = open(str_file, 'w')
    config = ConfigParser.SafeConfigParser()
    config.add_section("datasource")
    config.set("datasource", "dblink",
    "sqlite:////" + db_path_libreosteo)
    config.write(fp)
    fp.close()


class Configuration:
    """
    This class represents a wrapper around the configuration file.
    It allows to access directly on value from this object.
    """

    def __init__(self, str_file):
        """Create configuration object from path to file of configuration."""
        self.config = ConfigParser.SafeConfigParser()
        expanded_path = os.path.expanduser(str_file)
        if not os.path.isfile(expanded_path):
            create_default_config_file(expanded_path)
        self.config.read(expanded_path)

    def __getattr__(self, name):
        if self.config.has_section(name):
            return ConfigurationItem(self.config, name)
        else:
            return None

    def get_sections(self):
        """returns list of sections"""
        return self.config.sections()

    def get_values(self, name):
        """returns list of values for the section given by 'name'."""
        return self.config.items(name)

    def __len__(self):
        return len(self.config.sections())

    def get_default(self):
        """returns the default section has a list of values"""
        return self.config.defaults()


class ConfigurationItem:
    """
    This class represents a section into the configuration file.
    When you accessing to a section from the direct access of the
    configuration object, you obtain an instance of ConfigurationItem
    """

    def __init__(self, parent_config, section):
        """Builds the instance of ConfigurationItem which wraps the
        section.

        """
        self._parent = parent_config
        self._section = section

    def __getitem__(self, name):
        if self._parent.has_option(self._section, name):
            return self._parent.get(self._section, name)
        else:
            return None

    def __iter__(self):
        return self._parent.options(self._section)

    def __repr__(self):
        return str(self.__iter__())

    def __len__(self):
        return len(self.__iter__())
