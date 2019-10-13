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
# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from libreosteoweb.models import (TherapeutSettings, OfficeSettings, Invoice,
                                  Patient, Examination, InvoiceStatus,
                                  ExaminationStatus)
from datetime import datetime
from django.db.models import signals
from libreosteoweb.api.receivers import (block_disconnect_all_signal,
                                         receiver_examination,
                                         receiver_newpatient)


class TestChangeIdInvoice(APITestCase):
    def setUp(self):
        receivers_senders = [(receiver_examination, Examination),
                             (receiver_newpatient, Patient)]
        with block_disconnect_all_signal(signal=signals.post_save,
                                         receivers_senders=receivers_senders):
            self.user = User.objects.create_superuser("test", "test@test.com",
                                                      "testpw")
            TherapeutSettings.objects.create(adeli="12345",
                                             siret="12345",
                                             user=self.user)
            OfficeSettings.objects.create(office_siret="12345",
                                          currency='EUR',
                                          amount=50)
            self.client.login(username='test', password='testpw')
            self.p1 = Patient.objects.create(family_name="Picard",
                                             first_name="Jean-Luc",
                                             birth_date=datetime(1935, 7, 13))
            self.e1 = Examination.objects.create(date=datetime.now(),
                                                 status=0,
                                                 type=1,
                                                 patient=self.p1)

    def test_set_start_invoice_sequence_empty_value_no_invoice(self):
        response = self.client.get(reverse('officesettings-list'))
        settings = response.data[0]
        settings['invoice_start_sequence'] = 100
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_start_sequence'], u'100')
        response = self.client.get(reverse('officesettings-list')).data[0]
        self.assertEqual(response['invoice_start_sequence'], u'100')

    def test_no_set_start_invoice_sequence_on_already_set_value(self):
        OfficeSettings.objects.create(office_siret='12345',
                                      currency='EUR',
                                      amount=50,
                                      invoice_start_sequence=1000)
        response = self.client.get(reverse('officesettings-list'))
        settings = response.data[0]
        self.assertEqual(settings['invoice_start_sequence'], u'1000')
        settings['invoice_start_sequence'] = None
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.data['invoice_start_sequence'], u'1000')

    def test_set_start_invoice_sequence_invoice_set_limit(self):
        response = self.client.get(reverse('officesettings-list'))
        settings = response.data[0]
        settings['invoice_start_sequence'] = 100
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Invoice.objects.create(date=datetime.now(), amount=50, number=u'101')
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_set_start_invoice_sequence_create_invoice(self):
        response = self.client.get(reverse('officesettings-list'))
        settings = response.data[0]
        settings['invoice_start_sequence'] = 100
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'cash',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'100')
        response = self.client.get(reverse('officesettings-list'))
        settings = response.data[0]
        self.assertEqual(settings['invoice_start_sequence'], u'101')

        settings['invoice_start_sequence'] = 10
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        settings['invoice_start_sequence'] = 0
        response = self.client.put(reverse('officesettings-detail',
                                           kwargs={'pk': 1}),
                                   data=settings)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            OfficeSettings.objects.all()[0].invoice_start_sequence, u'101')


class TestCancelInvoice(APITestCase):
    def setUp(self):
        receivers_senders = [(receiver_examination, Examination),
                             (receiver_newpatient, Patient)]
        with block_disconnect_all_signal(signal=signals.post_save,
                                         receivers_senders=receivers_senders):
            self.user = User.objects.create_superuser("test", "test@test.com",
                                                      "testpw")
            TherapeutSettings.objects.create(adeli="12345",
                                             siret="12345",
                                             user=self.user)
            OfficeSettings.objects.create(office_siret="12345",
                                          currency='EUR',
                                          amount=50)
            self.client.login(username='test', password='testpw')
            self.p1 = Patient.objects.create(family_name="Picard",
                                             first_name="Jean-Luc",
                                             birth_date=datetime(1935, 7, 13))
            self.e1 = Examination.objects.create(date=datetime.now(),
                                                 status=0,
                                                 type=1,
                                                 patient=self.p1)

    def test_cancel_invoice(self):
        # Given
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'cash',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'10000')
        # When
        response = self.client.post(
            reverse('invoice-cancel',
                    kwargs={'pk': examination.invoices.latest('date').id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Then
        self.assertEqual(response.data['credit_note']['number'], u'10001')
        self.assertEqual(response.data['canceled']['status'],
                         InvoiceStatus.CANCELED)
        self.assertEqual(response.data['canceled']['canceled_by']['id'],
                         response.data['credit_note']['id'])
        self.assertEqual(response.data['canceled']['type'], 'invoice')
        self.assertEqual(response.data['credit_note']['type'], 'creditnote')
        credit_note = response.data['credit_note']

        # Retrieve the examination
        response = self.client.get(
            reverse('examination-detail', kwargs={'pk': self.e1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['invoice_number'])
        self.assertEqual(len(response.data['invoices_list']), 2)
        self.assertEqual(response.data['invoices_list'][0]['id'],
                         credit_note['id'])


class TestRegularizeNotPaidInvoice(APITestCase):
    def setUp(self):
        receivers_senders = [(receiver_examination, Examination),
                             (receiver_newpatient, Patient)]
        with block_disconnect_all_signal(signal=signals.post_save,
                                         receivers_senders=receivers_senders):
            self.user = User.objects.create_superuser("test", "test@test.com",
                                                      "testpw")
            TherapeutSettings.objects.create(adeli="12345",
                                             siret="12345",
                                             user=self.user)
            OfficeSettings.objects.create(office_siret="12345",
                                          currency='EUR',
                                          amount=50)
            self.client.login(username='test', password='testpw')
            self.p1 = Patient.objects.create(family_name="Picard",
                                             first_name="Jean-Luc",
                                             birth_date=datetime(1935, 7, 13))
            self.e1 = Examination.objects.create(date=datetime.now(),
                                                 status=0,
                                                 type=1,
                                                 patient=self.p1)

    def testRegularizeInvoiceNotPaid_Nominal(self):
        # Given
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'notpaid',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'10000')
        self.assertEqual(
            examination.invoices.latest('date').status,
            InvoiceStatus.WAITING_FOR_PAIEMENT)
        # When
        response = self.client.post(reverse(
            'examination-update-paiement',
            kwargs={'pk': examination.invoices.latest('date').id}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 60,
                                        'paiment_mode': 'check',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then
        invoice = Invoice.objects.filter(
            pk=examination.invoices.latest('date').id).first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.amount, 55)
        self.assertEqual(invoice.status, InvoiceStatus.INVOICED_PAID)
        paiements = invoice.paiment_set
        self.assertEqual(paiements.count(), 1)
        self.assertEqual(paiements.first().amount, 55)
        self.assertEqual(paiements.first().paiment_mode, 'check')
        self.assertEqual(paiements.first().currency, 'EUR')

    def testRegularizeInvoiceNotPaid_NotPaid(self):
        # Given
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'notpaid',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'10000')
        self.assertEqual(
            examination.invoices.latest('date').status,
            InvoiceStatus.WAITING_FOR_PAIEMENT)
        # When
        response = self.client.post(reverse(
            'examination-update-paiement',
            kwargs={'pk': examination.invoices.latest('date').id}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 60,
                                        'paiment_mode': 'notpaid',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then
        invoice = Invoice.objects.filter(
            pk=examination.invoices.latest('date').id).first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.amount, 55)
        self.assertEqual(invoice.status, InvoiceStatus.WAITING_FOR_PAIEMENT)
        paiements = invoice.paiment_set
        self.assertEqual(paiements.count(), 0)

    def testRegularizeInvoiceNotPaid_invalid(self):
        # Given
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'notpaid',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'10000')
        self.assertEqual(
            examination.invoices.latest('date').status,
            InvoiceStatus.WAITING_FOR_PAIEMENT)
        # When
        response = self.client.post(reverse(
            'examination-update-paiement',
            kwargs={'pk': examination.invoices.latest('date').id}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 60,
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Then
        invoice = Invoice.objects.filter(
            pk=examination.invoices.latest('date').id).first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.amount, 55)
        self.assertEqual(invoice.status, InvoiceStatus.WAITING_FOR_PAIEMENT)
        paiements = invoice.paiment_set
        self.assertEqual(paiements.count(), 0)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.status,
                         ExaminationStatus.WAITING_FOR_PAIEMENT)

    def testRegularizeAlreadyPaidInvoice(self):
        # Given
        response = self.client.post(reverse('examination-close',
                                            kwargs={'pk': self.e1.pk}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 55,
                                        'paiment_mode': 'cash',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.invoices.latest('date').number, u'10000')
        self.assertEqual(
            examination.invoices.latest('date').status,
            InvoiceStatus.INVOICED_PAID)
        # When
        response = self.client.post(reverse(
            'examination-update-paiement',
            kwargs={'pk': examination.invoices.latest('date').id}),
                                    data={
                                        'status': 'invoiced',
                                        'amount': 60,
                                        'paiment_mode' : 'check',
                                        'check': {}
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Then
        invoice = Invoice.objects.filter(
            pk=examination.invoices.latest('date').id).first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.amount, 55)
        self.assertEqual(invoice.status, InvoiceStatus.INVOICED_PAID)
        paiements = invoice.paiment_set
        self.assertEqual(paiements.count(), 0)
        examination = Examination.objects.filter(pk=self.e1.pk)[0]
        self.assertEqual(examination.status,
                         ExaminationStatus.INVOICED_PAID)


