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
# along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
from django.apps import AppConfig
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
            logger.debug(
                "Exception when purging files at starting application")

        try:
            nb_office_settings = models.OfficeSettings.objects.all().count()
            if nb_office_settings <= 0:
                default = models.OfficeSettings()
                default.save()
        except Exception:
            logger.warn("No database ready to initialize office settings")
