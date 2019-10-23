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
from libreosteoweb import models
from django.core.files.base import ContentFile
from datetime import datetime


def get_demonstration_file():
    demonstration_file = models.Document.objects.filter(
        title="demonstration").first()
    if demonstration_file is None:
        document_file = models.Document(
            title="demonstration",
            notes="This is a demonstration attached file",
            internal_date=datetime.today())
        document_file.document_file.save(
            'demonstration.txt',
            ContentFile(
                "For security purpose, no document could be uploaded on this demonstration instance"
            ))
        document_file.clean()
        document_file.save()
        demonstration_file = document_file
    return demonstration_file.document_file
