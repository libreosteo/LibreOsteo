
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
def enum(enumName, *listValueNames):
    listValueNumbers = range(len(listValueNames))
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    mainType = type(enumName, (), dictAttrib)
    return mainType

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
try :
    UNICODE_EXISTS = bool(type(unicode))
    _unicode = unicode
except NameError:
    _unicode = lambda s:str(s)
