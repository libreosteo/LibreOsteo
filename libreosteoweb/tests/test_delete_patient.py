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
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from libreosteoweb.models import Patient,Examination,TherapeutSettings,OfficeSettings,Invoice
from libreosteoweb.api.views import ExaminationViewSet,PatientViewSet
from datetime import datetime
from libreosteoweb.api.receivers import (
    block_disconnect_all_signal, receiver_examination, temp_disconnect_signal,
    receiver_newpatient)
from django.db.models import signals

class TestDeletePatient(APITestCase):
    def setUp(self):
        receivers_senders = [(receiver_examination, Examination), (receiver_newpatient, Patient)]
        with block_disconnect_all_signal(
                signal=signals.post_save,
                receivers_senders=receivers_senders
                ):
            self.user = User.objects.create_superuser("test","test@test.com", "testpw")
            TherapeutSettings.objects.create(adeli="12345",siret="12345", user=self.user)
            OfficeSettings.objects.create(office_siret="12345")
            self.p1 = Patient.objects.create(family_name="Picard", first_name="Jean-Luc", birth_date=datetime(1935,7,13))
            self.p2 = Patient.objects.create(family_name="Bond", first_name="James", birth_date=datetime(1924, 1, 1))
            self.e1 = Examination.objects.create(date=datetime.now(), status=0, type=1, patient=self.p1)
            # Invoice the examination
            self.client.login(username='test', password='testpw')
            response = self.client.post(reverse('examination-close', kwargs={'pk': self.e1.pk}), data={'status':'invoiced', 'amount':55, 'paiment_mode' : 'cash', 'check': {}}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_patient_with_invoiced_examination(self):
        response = self.client.delete(reverse('patient-detail', kwargs={'pk' : self.p1.pk})) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        assert len(Patient.objects.filter(id=self.p1.pk)) == 1
        assert len(Examination.objects.filter(patient=self.p1)) == 1

    def test_delete_patient_without_examination(self):
        response = self.client.delete(reverse('patient-detail', kwargs={'pk' : self.p2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        assert len(Patient.objects.filter(id=self.p2.pk)) == 0
        assert len(Examination.objects.filter(patient=self.p2)) == 0

    def test_delete_patient_with_invoiced_examination_gdpr(self):
        current_invoice = Examination.objects.filter(id=self.e1.pk)[0].invoices.latest('date')
        assert current_invoice is not None
        response = self.client.delete(reverse('patient-detail', kwargs={'pk' : self.p1.pk})+'?gdpr=True')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        assert len(Patient.objects.filter(id=self.p1.pk)) == 0
        assert len(Examination.objects.filter(id=self.e1.pk)) == 0
        assert len(Invoice.objects.filter(id=current_invoice.id)) == 1
        assert Invoice.objects.filter(id=current_invoice.id).first().patient_family_name == 'Picard'
       
