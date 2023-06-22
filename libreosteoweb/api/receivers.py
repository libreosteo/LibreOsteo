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
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import user_logged_in, user_logged_out
from ..models import OfficeEvent, Patient, Examination, PatientDocument, LoggedInUser
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class block_disconnect_all_signal():
    """Temporarily disconnect all managed models from a signal"""

    def __init__(self, signal, receivers_senders, dispatch_uid=None):
        self.signal = signal
        self.receivers_senders = receivers_senders
        self.dispatch_uid = dispatch_uid

    def __enter__(self):
        for (lreceiver, sender) in self.receivers_senders:
            self.signal.disconnect(receiver=lreceiver,
                                   sender=sender,
                                   dispatch_uid=self.dispatch_uid)

    def __exit__(self, type, value, traceback):
        for (lreceiver, sender) in self.receivers_senders:
            self.signal.connect(receiver=lreceiver,
                                sender=sender,
                                dispatch_uid=self.dispatch_uid)


class temp_disconnect_signal():
    """ Temporarily disconnect a model from a signal """

    def __init__(self, signal, receiver, sender, dispatch_uid=None):
        self.signal = signal
        self.receiver = receiver
        self.sender = sender
        self.dispatch_uid = dispatch_uid

    def __enter__(self):
        self.signal.disconnect(receiver=self.receiver,
                               sender=self.sender,
                               dispatch_uid=self.dispatch_uid)

    def __exit__(self, type, value, traceback):
        self.signal.connect(receiver=self.receiver,
                            sender=self.sender,
                            dispatch_uid=self.dispatch_uid)


@receiver(post_save, sender=Patient)
def receiver_newpatient(sender, **kwargs):
    event = OfficeEvent()
    event.clazz = Patient.__name__
    if kwargs['created']:
        event.type = Patient.TYPE_NEW_PATIENT
        event.comment = _('New patient created')
        event.reference = kwargs['instance'].id
        event.user = kwargs['instance'].current_user_operation
        event.clean()
        event.save()
    else:
        event.type = Patient.TYPE_UPDATE_PATIENT
        event.comment = _('Patient updated')
        event.reference = kwargs['instance'].id
        event.user = kwargs['instance'].current_user_operation
        event.clean()
        # Does not save update on patient
        # event.save()


@receiver(post_save, sender=Examination)
def receiver_examination(sender, **kwargs):
    event = OfficeEvent()
    event.clazz = Examination.__name__
    if kwargs['created']:
        event.type = kwargs['instance'].type
        event.comment = _('New examination')
        event.reference = kwargs['instance'].id
        event.user = kwargs['instance'].therapeut
        event.clean()
        event.save()


@receiver(post_delete, sender=PatientDocument)
def delete_document(sender, **kwargs):
    doc_instance = kwargs['instance']
    doc_instance.document.delete()


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
