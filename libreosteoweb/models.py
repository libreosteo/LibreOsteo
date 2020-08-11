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
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import date
from django.utils import timezone
from libreosteoweb.api.utils import enum
import mimetypes

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RegularDoctor(models.Model):
    """
        This class implements bean object to represent
        regular doctor for a patient

        It describes fields into this object which are mapped into DB
        """
    family_name = models.CharField(_('Family name'), max_length=200)
    first_name = models.CharField(_('Firstname'), max_length=200)
    phone = models.CharField(_('Phone'), max_length=100, blank=True, null=True)
    city = models.CharField(_('City'), max_length=200, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.family_name, self.first_name)


class Patient(models.Model):
    """
        This class implements bean object to represent
        patient.
        """
    family_name = models.CharField(_('Family name'), max_length=200)
    original_name = models.CharField(_('Original name'),
                                     max_length=200,
                                     blank=True)
    first_name = models.CharField(_('Firstname'), max_length=200, blank=True)
    birth_date = models.DateField(_('Birth date'))
    address_street = models.CharField(_('Street'), max_length=500, blank=True)
    address_complement = models.CharField(_('Address complement'),
                                          max_length=500,
                                          blank=True)
    address_zipcode = models.CharField(_('Zipcode'),
                                       max_length=200,
                                       blank=True)
    address_city = models.CharField(_('City'), max_length=200, blank=True)
    email = models.EmailField(_('Email'), max_length=200, blank=True)
    phone = models.CharField(_('Phone'), max_length=200, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'),
                                    max_length=200,
                                    blank=True)
    job = models.CharField(_('Job'), max_length=200, blank=True, default="")
    hobbies = models.TextField(_('Hobbies'), blank=True, default="")
    doctor = models.ForeignKey(RegularDoctor,
                               verbose_name=_('Regular doctor'),
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)
    smoker = models.BooleanField(_('Smoker'), default=False)
    laterality = models.CharField(_('Laterality'),
                                  max_length=1,
                                  choices=(('L', _('Left-handed')),
                                           ('R', _('Right-handed'))),
                                  blank=True,
                                  null=True)
    important_info = models.TextField(_('Important note'), blank=True)
    current_treatment = models.TextField(_('Current treatment'),
                                         blank=True,
                                         default="")
    surgical_history = models.TextField(_('Surgical history'), blank=True)
    medical_history = models.TextField(_('Medical history'), blank=True)
    family_history = models.TextField(_('Family history'), blank=True)
    trauma_history = models.TextField(_('Trauma history'), blank=True)
    medical_reports = models.TextField(_('Medical reports'), blank=True)
    creation_date = models.DateField(_('Creation date'),
                                     blank=True,
                                     null=True,
                                     editable=False)
    sex = models.CharField(_('Sex'),
                           max_length=1,
                           choices=(('M', _('Male')), ('F', _('Female'))),
                           blank=True,
                           null=True)

    # Not mapped field, only for traceability purpose
    current_user_operation = None

    def __unicode__(self):
        return "%s %s by %s" % (self.family_name, self.first_name,
                                self.current_user_operation)

    def clean(self):
        if self.creation_date is None:
            self.creation_date = date.today()

    def set_user_operation(self, user):
        """ Use this setting method to define the user
            which performs the operation (create, update).
            Not mapped in DB only for the runtime"""
        self.current_user_operation = user

    TYPE_NEW_PATIENT = 1
    TYPE_UPDATE_PATIENT = 2


class Children(models.Model):
    """
        This class implements bean object to represent
        children of a patient.
        """
    family_name = models.CharField(_('Family name'),
                                   max_length=200,
                                   blank=True)
    first_name = models.CharField(_('Firstname'), max_length=200)
    birthday_date = models.DateField(_('Birth date'))
    parent = models.ForeignKey(Patient, verbose_name=_('Parent'), on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s %s" % (self.family_name, self.first_name)


class Examination(models.Model):
    """
    This class implements bean object to represent
    examination on a patient
    """
    reason = models.TextField(_('Reason'), blank=True)
    reason_description = models.TextField(_('Reason description/Context'),
                                          blank=True)
    orl = models.TextField(_('ORL Sphere'), blank=True)
    visceral = models.TextField(_('Visceral Sphere'), blank=True)
    pulmo = models.TextField(_('Cardio-Pulmo Sphere'), blank=True)
    uro_gyneco = models.TextField(_('Uro-gyneco Sphere'), blank=True)
    periphery = models.TextField(_('Periphery Sphere'), blank=True)
    general_state = models.TextField(_('General state'), blank=True)
    medical_examination = models.TextField(_('Medical examination'),
                                           blank=True)
    diagnosis = models.TextField(_('Diagnosis'), blank=True)
    treatments = models.TextField(_('Treatments'), blank=True)
    conclusion = models.TextField(_('Conclusion'), blank=True)
    date = models.DateTimeField(_('Date'))
    # Status : 0 -> in progress
    # Status : 1 -> invoiced not paid
    # Status : 2 -> invoiced and paid
    # Status : 3 -> not invoiced
    status = models.SmallIntegerField(_('Status'))
    status_reason = models.TextField(_('Status reason'), blank=True, null=True)
    # Type : 1 -> normal examination
    # Type : 2 -> continuation of the examination
    # Type : 3 -> return of a previous examination
    # Type : 4 -> emergency examination
    type = models.SmallIntegerField(_('Type'))
    invoices = models.ManyToManyField('Invoice',
                                      verbose_name=_('Invoice'),
                                      blank=True)
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.PROTECT)
    therapeut = models.ForeignKey(User,
                                  verbose_name=_('Therapeut'),
                                  blank=True,
                                  null=True,
                                  on_delete=models.PROTECT)
    office = models.ForeignKey('OfficeSettings',
                               verbose_name=_('Office Settings'),
                               null=True,
                               on_delete=models.SET_NULL)

    EXAMINATION_IN_PROGRESS = 0
    EXAMINATION_WAITING_FOR_PAIEMENT = 1
    EXAMINATION_INVOICED_PAID = 2
    EXAMINATION_NOT_INVOICED = 3

    # i18n
    TYPE_NORMAL_EXAMINATION_I18N = _('Normal examination')
    TYPE_CONTINUING_EXAMINATION_I18N = _('Continuing examination')
    TYPE_RETURN_I18N = _('Return')
    TYPE_EMERGENCY_I18N = _('Emergency')

    def __unicode__(self):
        return "%s %s" % (self.patient, self.date)

    def get_invoice_number(self):
        invoice = self._get_last_invoice()
        return invoice.number if invoice is not None else None

    def _resolve_invoice(self, invoice):
        if invoice.canceled_by is not None:
            return self._resolve_invoice(invoice.canceled_by)
        return invoice if invoice.type == 'invoice' else None

    def _get_invoices_list(self):
        invoices_list = []
        if self.invoices is not None and self.invoices.all().count() > 0:
            invoices = self.invoices.all().order_by('date')
            for invoice in invoices:
                current_invoice = invoice
                invoices_list.append(current_invoice)
                while current_invoice.canceled_by is not None:
                    current_invoice = current_invoice.canceled_by
                    invoices_list.append(current_invoice)
        last_invoice = self._get_last_invoice()
        invoices_list.reverse()
        if last_invoice is not None:
            invoices_list.remove(self._get_last_invoice())
        return invoices_list

    invoices_list = property(_get_invoices_list)

    def _get_last_invoice(self):
        if self.invoices.all().count() == 0:
            return None
        invoices = self.invoices.all().order_by('-date')
        if invoices.first().canceled_by is not None:
            return self._resolve_invoice(invoices.first())
        return self.invoices.latest('date')

    last_invoice = property(_get_last_invoice)


ExaminationType = enum(
    'ExaminationType',
    'EMPTY',
    'NORMAL',
    'CONTINUING',
    'RETURN',
    'EMERGENCY',
)

ExaminationStatus = enum(
    'ExaminationStatus',
    'IN_PROGRESS',
    'WAITING_FOR_PAIEMENT',
    'INVOICED_PAID',
    'NOT_INVOICED',
)

InvoiceStatus = enum('InvoiceStatus', 'DRAFT', 'WAITING_FOR_PAIEMENT',
                     'INVOICED_PAID', 'CANCELED')


class ExaminationComment(models.Model):
    """This class represents a comment on examination
    """
    user = models.ForeignKey(User,
                             verbose_name=_('User'),
                             blank=True,
                             null=True,
                             on_delete=models.PROTECT)
    comment = models.TextField(_('Comment'))
    date = models.DateTimeField(_('Date'), null=True, blank=True)
    examination = models.ForeignKey(Examination, verbose_name=_('Examination'), on_delete=models.PROTECT)

class Invoice(models.Model):
    """
    This class implements bean object to represent
    invoice on an examination
    """
    date = models.DateTimeField(_('Date'))
    amount = models.FloatField(_('Amount'))
    currency = models.CharField(_('Currency'), max_length=10)
    paiment_mode = models.CharField(_('Paiment mode'), max_length=10)
    header = models.TextField(_('Header'), blank=True)
    therapeut_name = models.TextField(_('Therapeut name'))
    therapeut_first_name = models.TextField(_('Therapeut firstname'))
    quality = models.TextField(_('Quality'), blank=True)
    adeli = models.TextField(_('Adeli'))
    location = models.TextField(_('Location'))
    number = models.TextField(_('Number'))
    patient_family_name = models.CharField(_('Family name'), max_length=200)
    patient_original_name = models.CharField(_('Original name'),
                                             max_length=200,
                                             blank=True)
    patient_first_name = models.CharField(_('Firstname'),
                                          max_length=200,
                                          blank=True)
    patient_address_street = models.CharField(_('Street'),
                                              max_length=500,
                                              blank=True)
    patient_address_complement = models.CharField(_('Address complement'),
                                                  max_length=500,
                                                  blank=True)
    patient_address_zipcode = models.CharField(_('Zipcode'),
                                               max_length=200,
                                               blank=True)
    patient_address_city = models.CharField(_('City'),
                                            max_length=200,
                                            blank=True)
    content_invoice = models.TextField(_('Content'), blank=True)
    footer = models.TextField(_('Footer'), blank=True)
    office_siret = models.TextField(_('Siret'), blank=True)
    office_address_street = models.CharField(_('Street'),
                                             max_length=500,
                                             blank=True,
                                             default='')
    office_address_complement = models.CharField(_('Address complement'),
                                                 max_length=500,
                                                 blank=True,
                                                 default='')
    office_address_zipcode = models.CharField(_('Zipcode'),
                                              max_length=200,
                                              blank=True,
                                              default='')
    office_address_city = models.CharField(_('City'),
                                           max_length=200,
                                           blank=True,
                                           default='')
    office_phone = models.CharField(_('Phone'),
                                    max_length=200,
                                    blank=True,
                                    default='')
    status = models.IntegerField(_('status'), default=0)
    therapeut_id = models.IntegerField(_('therapeut_id'), default=0)
    canceled_by = models.ForeignKey('self',
                                    verbose_name=_("Canceled by"),
                                    blank=True,
                                    null=True,
                                    on_delete=models.PROTECT)
    type = models.CharField(_('Invoice type'),
                            max_length=10,
                            blank=True,
                            default='invoice')

    officesettings_id = models.IntegerField(_('office id'), default=1)
    check_sum = models.BinaryField(_('check_sum'), max_length=256)

    def _get_paiments_list(self):
        return self.paiment_set.all().order_by('-date')

    paiments_list = property(_get_paiments_list)

    def clean(self):
        if self.date is None:
            self.date = timezone.now()

    class Meta:
        ordering = ['-date']


class PaimentMean(models.Model):
    """
    This class implements object to represent
    the mean of paiement of an examination
    """
    code = models.CharField(_('Code'), max_length=10)
    text = models.CharField(_('Text'), max_length=50)
    enable = models.BooleanField(_('Enabled'), default=True)


class Paiment(models.Model):
    """
    This class implements object to represent
    paiments (it is possible to have many paiments) of an invoice
    """
    invoice = models.ManyToManyField('Invoice',
                                     verbose_name=_("Invoices"),
                                     blank=True)
    amount = models.FloatField(_('Amount'))
    currency = models.CharField(_('Currency'), max_length=10)
    paiment_mode = models.CharField(_('Paiment mode'), max_length=10)
    date = models.DateField(_('Date'))


class OfficeEvent(models.Model):
    """
    This class implements bean object to represent
    event on the office
    """
    date = models.DateTimeField(_('Date'), blank=True)
    clazz = models.TextField(_('Class'), blank=True)
    type = models.SmallIntegerField(_('Type'))
    comment = models.TextField(_('Comment'), blank=True)
    reference = models.IntegerField(_('Reference'), blank=True, null=False)
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             blank=True,
                             null=False,
                             on_delete=models.PROTECT)

    def clean(self):
        if self.date is None:
            self.date = timezone.now()


class OfficeSettings(models.Model):
    """
    This class implements model for the settings into the application
    """
    office_name = models.CharField(_('Office name'), max_length=250, blank=True, null=True)
    invoice_office_header = models.CharField(_('Invoice office header'),
                                             max_length=500,
                                             blank=True)
    office_address_street = models.CharField(_('Street'),
                                             max_length=500,
                                             blank=True)
    office_address_complement = models.CharField(_('Address complement'),
                                                 max_length=500,
                                                 blank=True)
    office_address_zipcode = models.CharField(_('Zipcode'),
                                              max_length=200,
                                              blank=True)
    office_address_city = models.CharField(_('City'),
                                           max_length=200,
                                           blank=True)
    office_phone = models.CharField(_('Phone'), max_length=200, blank=True)
    office_siret = models.CharField(_('Siret'), max_length=20)
    amount = models.FloatField(_('Amount'),
                               blank=True,
                               null=True,
                               default=None)
    currency = models.CharField(_('Currency'), max_length=10)
    invoice_content = models.TextField(_('Invoice content'), blank=True)
    invoice_footer = models.TextField(_('Invoice footer'), blank=True)
    invoice_start_sequence = models.TextField(_('Invoice start sequence'),
                                              blank=True)

    UPDATE_INVOICE_SEQUENCE = 1


class TherapeutSettings(models.Model):
    """
    This class implements model for extending the User model
    """
    adeli = models.TextField(_('Adeli'), blank=True)
    quality = models.TextField(_('Quality'), blank=True)
    user = models.OneToOneField(User,
                                verbose_name=_('User'),
                                blank=True,
                                null=True,
                                on_delete=models.PROTECT)
    siret = models.CharField(_('Siret'), max_length=20, blank=True, null=True)
    invoice_footer = models.TextField(_('Invoice footer'),
                                      blank=True,
                                      null=True)

    # dashboard modules
    stats_enabled = models.BooleanField(_('Statistics'), default=True)
    last_events_enabled = models.BooleanField(_('Events history'),
                                              default=True)

    # Examination view modules
    spheres_enabled = models.BooleanField(_('Spheres'), default=True)
    zipcode_completion_enabled = models.BooleanField(_('Zipcode completion (France)'), default=True)


    MODULES_FIELDS = [
        {
            'name':
            _('Dashboard'),
            'modules': [
                {
                    'field': stats_enabled,
                    'image': 'images/dashboard-stats.png'
                },
                {
                    'field': last_events_enabled,
                    'image': 'images/dashboard-events.png'
                },
            ]
        },
        {
            'name':
            _('Examination'),
            'modules': [
                {
                    'field': spheres_enabled,
                    'image': 'images/examination-spheres.png'
                },
                {
                    'field': zipcode_completion_enabled,
                    'image': 'images/zipcode-completion.png'
                },
            ]
        },
    ]

    def save(self, *args, **kwargs):
        """
        Ensure that empty string are none in DB
        """
        if self.siret == '':
            self.siret = None
        if self.invoice_footer == '':
            self.invoice_footer = None
        super(TherapeutSettings, self).save(*args, **kwargs)


class FileImport(models.Model):
    """
    implements a couple of file for importing data.
    It concerns only Patient and examination
    """
    file_patient = models.FileField(_('Patient file'))
    file_examination = models.FileField(_('Examination file'), blank=True)
    status = models.IntegerField(_('validity status'),
                                 blank=True,
                                 default=None,
                                 null=True)
    analyze = None

    def delete(self, *args, **kwargs):
        """
        Delete media file too.
        """
        if bool(self.file_patient):
            storage_patient, path_patient = self.file_patient.storage, self.file_patient.path
        if bool(self.file_examination):
            storage_examination, path_examination = self.file_examination.storage, self.file_examination.path
        super(FileImport, self).delete(*args, **kwargs)
        if bool(self.file_patient):
            storage_patient.delete(path_patient)
        if bool(self.file_examination):
            storage_examination.delete(path_examination)



class Document(models.Model):
    """
    Implements a document to be attached to
    an examination or patient file
    """
    document_file = models.FileField(_('Document file'), upload_to="documents")
    title = models.TextField(_('Title'))
    notes = models.TextField(_('Notes'), blank=True, null=True, default=None)
    internal_date = models.DateTimeField(_('Adding date'),
                                         blank=True,
                                         null=False)
    document_date = models.DateField(_('Document date'),
                                     blank=True,
                                     null=True,
                                     default=None)
    user = models.ForeignKey(User,
                             verbose_name=_('User'),
                             blank=True,
                             null=True,
                             on_delete=models.PROTECT)
    mime_type = models.TextField(_('Mime-Type'),
                                 blank=False,
                                 null=True,
                                 default=None)

    def delete(self, *args, **kwargs):
        """
        Delete the file
        """
        super(Document, self).delete(*args, **kwargs)
        storage_document, path_document = self.document_file.storage, self.document_file.path
        storage_document.delete(path_document)

    def clean(self):
        if self.internal_date is None:
            self.internal_date = timezone.now()
        self.mime_type = mimetypes.guess_type(self.document_file.path)[0]
        logger.info("mime_type = %s " % self.mime_type)


class PatientDocument(models.Model):
    """
    Implements a document to be attached to a patient file
    """
    patient = models.ForeignKey(Patient,
                                verbose_name=_('patient'),
                                on_delete=models.CASCADE)
    document = models.OneToOneField(Document,
                                    verbose_name=_('document'),
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    attachment_type = models.SmallIntegerField(_('attachmentType'))

    AttachmentType = enum('AttachmentType', 'SURGICAL', 'MEDICAL', 'FAMILIAL',
                          'TRAUMA', 'MEDICAL_REPORTS')

    def delete(self, *args, **kwargs):
        super(PatientDocument, self).delete(*args, **kwargs)
        self.document.delete()
