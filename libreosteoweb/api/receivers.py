from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from ..models import OfficeEvent, Patient, Examination



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