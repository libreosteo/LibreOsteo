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

from libreosteoweb.models import OfficeSettings, OfficeEvent
from django.utils.translation import gettext_lazy as _
from libreosteoweb.api.utils import _unicode
import logging

logger = logging.getLogger(__name__)


def settings_event_tracer(officesettings, user, new_value):
    if officesettings.invoice_start_sequence is not None and len(officesettings.invoice_start_sequence) != 0 \
            and officesettings.invoice_start_sequence != new_value :
        event = OfficeEvent()
        event.clazz = OfficeSettings.__name__
        event.type = OfficeSettings.UPDATE_INVOICE_SEQUENCE
        event.comment = _(
            'Invoice sequence updated from %(previous)s to %(actual)s') % {
                'previous': _unicode(officesettings.invoice_start_sequence),
                'actual': _unicode(new_value)
            }
        event.reference = officesettings.id
        event.user = user
        event.clean()
        event.save()


def full_retrieve_patient_list(user):
    event = OfficeEvent()
    event.clazz = OfficeSettings.__name__
    event.type = OfficeSettings.DOWNLOAD_PATIENT_LIST
    event.comment = _('%s has downloaded the full list of patient') %\
                      user.username
    event.reference = user.id
    event.user = user
    event.clean()
    event.save()


def full_db_download(user):
    event = OfficeEvent()
    event.clazz = OfficeSettings.__name__
    event.type = OfficeSettings.DOWNLOAD_FULL_DB
    event.comment = _('%s has downloaded the full content of the Database') %\
                      user.username
    event.reference = user.id
    event.user = user
    event.clean()
    event.save()
