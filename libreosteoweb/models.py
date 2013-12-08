from django.db import models
from django.utils.translation import ugettext_lazy as _


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
        smoker = models.BooleanField(_('Smoker'))
        important_info = models.TextField(_('Important note'), blank=True)
        surgical_history = models.TextField(_('Surgical history'), blank=True)
        medical_history = models.TextField(_('Medical history'), blank=True)
        family_history = models.TextField(_('Family history'), blank=True)
        trauma_history = models.TextField(_('Trauma history'), blank=True)

        def __unicode__(self):
                return "%s %s" % (self.family_name, self.first_name)


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