from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from datetime import date


class RegularDoctor(models.Model):
        """
        This class implements bean object to represent
        regular doctor for a patient

        It describes fields into this object which are mapped into DB
        """
        family_name = models.CharField(_('Family name'), max_length=200)
        first_name = models.CharField(_('Firstname'), max_length=200)
        phone = models.CharField(_('Phone'), max_length=100, blank=True)
        city = models.CharField(_('City'), max_length=200, blank=True)

        def __unicode__(self):
                return "%s %s" % (self.family_name, self.first_name)


class Patient(models.Model):
        """
        This class implements bean object to represent
        patient.
        """
        family_name = models.CharField(_('Family name'), max_length=200 )
        original_name = models.CharField(_('Original name'), max_length=200, blank=True)
        first_name = models.CharField(_('Firstname'), max_length=200, blank=True )
        birth_date = models.DateField(_('Birth date'))
        address_street = models.CharField(_('Street'), max_length=500, blank=True)
        address_complement = models.CharField(_('Address complement'), max_length=500, blank=True)
        address_zipcode = models.CharField(_('Zipcode'), max_length=200, blank=True)
        address_city = models.CharField(_('City'), max_length=200, blank=True)
        phone = models.CharField(_('Phone'), max_length=200, blank=True)
        mobile_phone = models.CharField(_('Mobile phone'), max_length=200, blank=True)
        #family_situation = Column(Integer)
        doctor = models.ForeignKey(RegularDoctor, verbose_name=_('Regular doctor'), blank=True, null=True)
        smoker = models.BooleanField(_('Smoker'), default=False)
        important_info = models.TextField(_('Important note'), blank=True)
        surgical_history = models.TextField(_('Surgical history'), blank=True)
        medical_history = models.TextField(_('Medical history'), blank=True)
        family_history = models.TextField(_('Family history'), blank=True)
        trauma_history = models.TextField(_('Trauma history'), blank=True)
        medical_reports = models.TextField(_('Medical reports'), blank=True)
        creation_date = models.DateField(_('Creation date'), blank=True, null=True, editable=False)

        def __unicode__(self):
                return "%s %s" % (self.family_name, self.first_name)

        def validate_unique(self, *args, **kwargs):
            super(Patient, self).validate_unique(*args, **kwargs)
            found = Patient.objects.filter(family_name__iexact=self.family_name)\
                    .filter( first_name__iexact=self.first_name )\
                    .filter( birth_date__iexact=self.birth_date )\
                    .exclude( id = self.id)\
                    .exists()
            if found:
                raise ValidationError(
                    {
                        NON_FIELD_ERRORS:
                        _('This patient already exists')
                    }
                )

        def clean(self):
            if self.birth_date > date.today():
                raise ValidationError({
                    'birth_date' :
                        _('Birth date is invalid')
                })

            if self.creation_date is None:
                self.creation_date = date.today()


class Children(models.Model):
        """
        This class implements bean object to represent
        children of a patient.
        """
        family_name = models.CharField(_('Family name'), max_length=200, blank=True)
        first_name = models.CharField(_('Firstname'), max_length=200)
        birthday_date = models.DateField(_('Birth date'))
        parent = models.ForeignKey(Patient, verbose_name=_('Parent'))

        def __unicode__(self):
                return "%s %s" % (self.family_name, self.first_name)

class Examination(models.Model):
    """
    This class implements bean object to represent
    examination on a patient
    """
    reason = models.TextField(_('Reason'), blank=True)
    reason_description = models.TextField(_('Reason description'), blank=True)
    orl = models.TextField(_('ORL Sphere'), blank=True)
    visceral = models.TextField(_('Visceral Sphere'), blank=True)
    pulmo = models.TextField(_('Cardio-Pulmo Sphere'), blank=True)
    uro_gyneco = models.TextField(_('Uro-gyneco Sphere'), blank=True)
    periphery = models.TextField(_('Periphery Sphere'), blank=True)
    general_state = models.TextField(_('General state'), blank=True)
    medical_examination = models.TextField(_('Medical examination'), blank=True)
    diagnosis = models.TextField(_('Diagnosis'), blank=True)
    treatments = models.TextField(_('Treatments'), blank=True)
    conclusion = models.TextField(_('Conclusion'), blank=True)
    date = models.DateTimeField(_('Date'))
    # Status : 0 -> in progress
    # Status : 1 -> invoiced not paid
    # Status : 2 -> invoiced and paid
    # Status : 3 -> not invoiced
    status = models.SmallIntegerField(_('Status'))
    # Type : 1 -> normal examination
    # Type : 2 -> Scheduled return
    # Type : 3 -> Urgent return
    type = models.SmallIntegerField(_('Type'))
    #invoice =
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'))
    therapeut = models.ForeignKey(User, verbose_name=_('Therapeut'), blank=True,null=True)

EXAMINATION_IN_PROGRESS = 0
EXAMINATION_WAITING_FOR_PAIEMENT = 1
EXAMINATION_INVOICED_PAID = 2
EXAMINATION_NOT_INVOICED = 3