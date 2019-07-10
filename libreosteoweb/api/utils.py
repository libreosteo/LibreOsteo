
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
import socket
import netifaces
import logging 

logger = logging.getLogger(__file__)
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

class NetworkHelper():
    def get_all_addresses(self):
        addresses = []
        try :
            addresses = [netifaces.ifaddresses(it)[netifaces.AF_INET][0]['addr'] for it in netifaces.interfaces() if netifaces.AF_INET in netifaces.ifaddresses(it) ]
        except :
            logger.exception("Cannot obtain address on the host")
        return addresses

    def get_bound_addresses(self, addresses, port):
        return [a for a in addresses if self._check_socket(a, port)]

    def _check_socket(self, addr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((addr, int(port))) == 0
        sock.close()
        return result

def convert_to_long(value):
    try:
        return long(value)
    except:
        return int(value)
