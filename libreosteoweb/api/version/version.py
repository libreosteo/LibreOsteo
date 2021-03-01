# This file is part of LibreOsteo.
#
# LibreOsteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibreOsteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.import urllib.request
import json
import logging
import libreosteoweb
from packaging.version import parse
import urllib

logger = logging.getLogger()


def ask_for_new_version():
    try:
        logger.info("Ask for new version")
        with urllib.request.urlopen(
                "https://www.libreosteo.org/api/version") as f:
            contents = f.read().decode("utf-8")
            version = json.loads(contents)
            logger.info("version read = %s " % version['version'])
            if parse(version['version']) > parse(libreosteoweb.__version__):
                return (True, version['version'])
    except Exception as ex:
        logger.error("Cannot access to version checking", ex)
    return (False, None)
