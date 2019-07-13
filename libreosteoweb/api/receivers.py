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
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.utils.translation import ugettext_lazy as _
from ..models import OfficeEvent, Patient, Examination, PatientDocument
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
		for (receiver, sender) in self.receivers_senders:
			self.signal.disconnect(
				receiver=receiver,
				sender=sender,
				dispatch_uid=self.dispatch_uid
				)
	def __exit__(self, type, value, traceback):
		for(receiver, sender) in self.receivers_senders:
			self.signal.connect(
				receiver=receiver,
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
        self.signal.disconnect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid
        )

    def __exit__(self, type, value, traceback):
        self.signal.connect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid
        )

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
