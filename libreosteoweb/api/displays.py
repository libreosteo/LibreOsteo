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
from django.shortcuts import render
from django.forms.models import ModelForm
from libreosteoweb import models
from django.contrib.auth.models import User
from django.conf import settings
import libreosteoweb
from .permissions import maintenance_available
from django.views.decorators.cache import never_cache
from libreosteoweb.api.version import version

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def filter_fields(f):
    return f is not None and f.formfield() is not None


class GenericDisplay(ModelForm):
    class Meta:
        model = User
        fields = [f.name for f in model._meta.fields if f.editable]

    def display_fields(self):
        return dict([
            (f.name, f.formfield().label)
            for f in filter(filter_fields, self.Meta.model._meta.fields)
        ])


class PatientDisplay(GenericDisplay):
    class Meta:
        model = models.Patient
        fields = [f.name for f in model._meta.fields if f.editable]


class RegularDoctorDisplay(GenericDisplay):
    class Meta:
        model = models.RegularDoctor
        fields = [f.name for f in model._meta.fields if f.editable]


class ExaminationDisplay(GenericDisplay):
    class Meta:
        model = models.Examination
        fields = [f.name for f in model._meta.fields if f.editable]


class UserDisplay(GenericDisplay):
    class Meta:
        model = User
        fields = [f.name for f in model._meta.fields if f.editable]


class TherapeutSettingsDisplay(GenericDisplay):
    class Meta:
        model = models.TherapeutSettings
        fields = [f.name for f in model._meta.fields if f.editable]


class OfficeSettingsDisplay(GenericDisplay):
    class Meta:
        model = models.OfficeSettings
        fields = [f.name for f in model._meta.fields if f.editable]


def display_invoices(request):
    return render(request, "partials/invoice-list.html", {})


def display_index(request):
    new_version_available, new_version = version.ask_for_new_version()
    return render(
        request, 'index.html', {
            'version': libreosteoweb.__version__,
            'request': request,
            'new_version_available': new_version_available,
            'new_version': new_version
        })


def display_patient(request):
    display = PatientDisplay()
    displayExamination = ExaminationDisplay()
    return render(
        request, 'partials/patient-detail.html', {
            'patient': display.display_fields(),
            'examination': displayExamination.display_fields()
        })


def display_newpatient(request):
    display = PatientDisplay()
    return render(request, 'partials/add-patient.html',
                  {'patient': display.display_fields()})


def display_doctor(request):
    display = RegularDoctorDisplay()
    return render(request, 'partials/doctor-modal-add.html',
                  {'doctor': display.display_fields()})


def display_examination_timeline(request):
    display = ExaminationDisplay()
    return render(request, 'partials/timeline.html',
                  {'examination': display.display_fields()})


def display_examination(request):
    displayExamination = ExaminationDisplay()
    return render(request, 'partials/examination.html',
                  {'examination': displayExamination.display_fields()})


def display_search_result(request):
    return render(request, 'partials/search-result.html', {})


def display_userprofile(request):
    displayUser = UserDisplay()
    displayTherapeutSettings = TherapeutSettingsDisplay()
    return render(
        request, 'partials/user-profile.html', {
            'user': displayUser.display_fields(),
            'therapeutsettings': displayTherapeutSettings.display_fields(),
            'dashboard_modules':
            models.TherapeutSettings.DASHBOARD_MODULES_FIELDS,
            'DEMONSTRATION': settings.DEMONSTRATION
        })


def display_dashboard(request):
    therapeut_settings, _ = models.TherapeutSettings.objects.get_or_create(
        user=request.user)
    return render(request, 'partials/dashboard.html', {
        'therapeutsettings': therapeut_settings,
    })


def display_officeevent(request):
    return render(request, 'partials/officeevent.html', {})


def display_invoicing(request):
    return render(request, 'partials/invoice-modal.html', {})


def display_officesettings(request):
    displayOfficeSettings = OfficeSettingsDisplay()
    return render(
        request, 'partials/office-settings.html', {
            'officesettings': displayOfficeSettings.display_fields,
            'user': request.user
        })


def display_adduser(request):
    return render(request, 'partials/add-user-modal.html', {})


def display_setpassword(request):
    return render(request, 'partials/set-password-user-modal.html', {})


def display_import_files(request):
    return render(request, 'partials/import-file.html', {'request': request})


def display_rebuild_index(request):
    return render(request, 'partials/rebuild-index.html', {'request': request})


def display_file_manager(request):
    return render(request, 'partials/filemanager.html', {'request': request})


def display_confirmation(request):
    return render(request, 'partials/confirmation.html')


@never_cache
@maintenance_available()
def display_restore(request):
    return render(request, 'partials/restore.html', {'request': request})


@never_cache
@maintenance_available()
def display_register(request):
    return render(request, 'partials/register.html', {'request': request})
