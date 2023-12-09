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
from libreosteoweb import models
from libreosteoweb.api.utils import _unicode, convert_to_long
from django.utils import timezone


class Generator(object):

    def __init__(self, office_settings, therapeut_settings):
        self.office_settings = office_settings
        self.therapeut_settings = therapeut_settings

    def generate_invoice(self, examination, serializer_data, user_therapeut):
        invoice = models.Invoice()
        invoice.amount = serializer_data['amount']
        invoice.currency = self.office_settings.currency
        invoice.header = self.office_settings.invoice_office_header
        invoice.office_address_street = self.office_settings.office_address_street
        invoice.office_address_complement = self.office_settings.office_address_complement
        invoice.office_address_zipcode = self.office_settings.office_address_zipcode
        invoice.office_address_city = self.office_settings.office_address_city
        invoice.office_phone = self.office_settings.office_phone
        invoice.office_siret = self.office_settings.office_siret

        # Override the siret on the invoice with the therapeut siret if defined
        if self.therapeut_settings.siret is not None:
            invoice.office_siret = self.therapeut_settings.siret

        invoice.paiment_mode = serializer_data['paiment_mode']
        invoice.therapeut_name = user_therapeut.last_name
        invoice.therapeut_first_name = user_therapeut.first_name
        invoice.therapeut_id = user_therapeut.id
        invoice.quality = self.therapeut_settings.quality
        invoice.professional_id = self.therapeut_settings.professional_id
        invoice.professional_id_label = self.office_settings.professional_id_label
        invoice.location = self.office_settings.office_address_city

        invoice.patient_family_name = examination.patient.family_name
        invoice.patient_original_name = examination.patient.original_name
        invoice.patient_first_name = examination.patient.first_name
        invoice.patient_address_street = examination.patient.address_street
        invoice.patient_address_complement = examination.patient.address_complement
        invoice.patient_address_zipcode = examination.patient.address_zipcode
        invoice.patient_address_city = examination.patient.address_city
        invoice.content_invoice = self.office_settings.invoice_content
        invoice.footer = self.office_settings.invoice_footer

        # Override the footer on the invoice with the therapeut settings if defined
        if self.therapeut_settings.invoice_footer is not None:
            invoice.footer = self.therapeut_settings.invoice_footer
        invoice.number = self.get_invoice_number()
        invoice.date = timezone.now()
        invoice.officesettings_id = self.office_settings.id
        return invoice

    def get_invoice_number(self):
        if self.office_settings.invoice_start_sequence is not None and len(
                self.office_settings.invoice_start_sequence) > 0:
            invoice_number = _unicode(
                convert_to_long(self.office_settings.invoice_start_sequence))
            self.office_settings.invoice_start_sequence = _unicode(
                convert_to_long(invoice_number) + 1)
        else:
            invoice_number = _unicode(10000)
            self.office_settings.invoice_start_sequence = _unicode(
                convert_to_long(invoice_number) + 1)
        if self.office_settings.invoice_prefix_sequence is not None:
            invoice_number = self.office_settings.invoice_prefix_sequence + invoice_number
        return invoice_number

    def cancel_invoice(self, invoice):
        credit_note = models.Invoice()
        credit_note.amount = -1 * invoice.amount
        credit_note.currency = invoice.currency
        credit_note.header = invoice.header
        credit_note.office_address_street = invoice.office_address_street
        credit_note.office_address_complement = invoice.office_address_complement
        credit_note.office_address_zipcode = invoice.office_address_zipcode
        credit_note.office_address_city = invoice.office_address_city
        credit_note.office_phone = invoice.office_phone
        credit_note.office_siret = invoice.office_siret
        credit_note.paiment_mode = invoice.paiment_mode
        credit_note.therapeut_name = invoice.therapeut_name
        credit_note.therapeut_first_name = invoice.therapeut_first_name
        credit_note.therapeut_id = invoice.therapeut_id
        credit_note.quality = invoice.quality
        credit_note.professional_id = invoice.professional_id
        credit_note.professional_id_label = invoice.professional_id_label
        credit_note.location = invoice.location
        credit_note.patient_family_name = invoice.patient_family_name
        credit_note.patient_original_name = invoice.patient_original_name
        credit_note.patient_first_name = invoice.patient_first_name
        credit_note.patient_address_street = invoice.patient_address_street
        credit_note.patient_address_complement = invoice.patient_address_complement
        credit_note.patient_address_zipcode = invoice.patient_address_zipcode
        credit_note.patient_address_city = invoice.patient_address_city
        credit_note.content_invoice = invoice.content_invoice
        credit_note.footer = invoice.footer
        credit_note.date = timezone.now()
        credit_note.type = 'creditnote' if credit_note.amount < 0 else 'invoice'
        credit_note.number = self.get_invoice_number()
        credit_note.status = models.InvoiceStatus.INVOICED_PAID
        credit_note.officesettings_id = invoice.officesettings_id
        return credit_note


class ExaminationInvoiceHelper(object):

    def __init__(self, office_settings, therapeut_settings, therapeut_user):
        self.office_settings = office_settings
        self.therapeut_settings = therapeut_settings
        self.therapeut_user = therapeut_user

    def invoice_examination(self,
                            invoicing_serializer,
                            current_examination,
                            invoice_to_cancel=None):
        if hasattr(invoicing_serializer,
                   'initial_data') and not invoicing_serializer.is_valid():
            return {'errors': invoicing_serializer.errors}

        if invoicing_serializer.validated_data['status'] == 'notinvoiced':
            current_examination.status = models.Examination.EXAMINATION_NOT_INVOICED
            current_examination.status_reason = invoicing_serializer.validated_data[
                'reason']
            current_examination.save()
            return {'invoiced': None}
        if invoicing_serializer.validated_data['status'] == 'invoiced':
            current_invoice = self.generate_invoice(
                current_examination, invoicing_serializer.validated_data,
                invoice_to_cancel)
            current_examination.invoices.add(current_invoice)
            if invoicing_serializer.validated_data[
                    'paiment_mode'] == 'notpaid':
                current_examination.status = models.ExaminationStatus.WAITING_FOR_PAIEMENT
                current_invoice.status = models.InvoiceStatus.WAITING_FOR_PAIEMENT
                current_invoice.save()
                current_examination.save()
            if invoicing_serializer.validated_data['paiment_mode'] in [
                    p.code
                    for p in models.PaimentMean.objects.filter(enable=True)
            ]:
                current_examination.status = models.ExaminationStatus.INVOICED_PAID
                current_invoice.status = models.InvoiceStatus.INVOICED_PAID
                current_invoice.save()
                current_examination.save()
            return {'invoiced': current_invoice.id}
        return {}

    def generate_invoice(self, examination, invoicingSerializerData,
                         invoice_to_cancel):
        invoice = Generator(self.office_settings,
                            self.therapeut_settings).generate_invoice(
                                examination, invoicingSerializerData,
                                self.therapeut_user)
        self.office_settings.save()
        invoice.save()
        if invoice_to_cancel:
            invoice_to_cancel.status = models.InvoiceStatus.CANCELED
            invoice_to_cancel.canceled_by = invoice
            invoice.replace = invoice_to_cancel.number
            invoice_to_cancel.save()
            invoice.save()
        return invoice
