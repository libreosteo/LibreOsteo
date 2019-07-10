
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
from django.apps import AppConfig
from sqlite3 import OperationalError
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class LibreosteoConfig(AppConfig):
    name = 'libreosteoweb'
    verbose_name = "Libreosteo WebApp"

    def ready(self):
        import libreosteoweb.api.receivers
        import libreosteoweb.models as models
        file_import_list = models.FileImport.objects.all()
        try:
            for f in file_import_list:
                f.delete()
        except Exception:
            logger.debug("Exception when purging files at starting application")
    
        try:
            office_settings_list = models.OfficeSettings.objects.all()
            if len(office_settings_list) <= 0 :
                default = models.OfficeSettings()
                default.save()
        except Exception:
            logger.warn("No database ready to initialize office settings")
