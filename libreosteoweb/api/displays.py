from django.shortcuts import render_to_response
from django.forms.models import ModelForm
from libreosteoweb import models 
from django.contrib.auth.models import User


def filter_fields(f):
    return f is not None and f.formfield() is not None

class PatientDisplay(ModelForm):
    class Meta:
        model = models.Patient

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, models.Patient._meta.fields)])

class RegularDoctorDisplay(ModelForm):
    class Meta:
        model = models.RegularDoctor

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, models.RegularDoctor._meta.fields)])

class ExaminationDisplay(ModelForm):
    class Meta:
        model = models.Examination

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, models.Examination._meta.fields)])

class UserDisplay(ModelForm):
    class Meta:
        model = User

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, User._meta.fields)])

class TherapeutSettingsDisplay(ModelForm):
    class Meta:
        model = models.TherapeutSettings

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, models.TherapeutSettings._meta.fields)])

class OfficeSettingsDisplay(ModelForm):
    class Meta:
        model = models.OfficeSettings

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, models.OfficeSettings._meta.fields)])

def display_patient(request):
    display = PatientDisplay()
    displayExamination = ExaminationDisplay()
    return render_to_response('partials/patient-detail.html', {'patient' : display.display_fields,
                                                               'examination' : displayExamination.display_fields})

def display_newpatient(request):
    display = PatientDisplay()
    return render_to_response('partials/add-patient.html', {'patient' : display.display_fields})

def display_doctor(request):
    display = RegularDoctorDisplay()
    return render_to_response('partials/doctor-modal-add.html', {'doctor':display.display_fields})

def display_examination_timeline(request):
    display = ExaminationDisplay()
    return render_to_response('partials/timeline.html', {'examination' : display.display_fields})

def display_examination(request):
    displayExamination = ExaminationDisplay()
    return render_to_response('partials/examination.html', {'examination' : displayExamination.display_fields})

def display_search_result(request):
    return render_to_response('partials/search-result.html', {})

def display_userprofile(request):
    displayUser = UserDisplay()
    displayTherapeutSettings = TherapeutSettingsDisplay()
    return render_to_response('partials/user-profile.html', {'user' : displayUser.display_fields, 
        'therapeutsettings': displayTherapeutSettings.display_fields})

def display_dashboard(request):
    return render_to_response('partials/dashboard.html', {})

def display_officeevent(request):
    return render_to_response('partials/officeevent.html', {})

def display_invoicing(request):
    return render_to_response('partials/invoice-modal.html', {})

def display_officesettings(request):
    displayOfficeSettings = OfficeSettingsDisplay()
    return render_to_response('partials/office-settings.html', {'officesettings' : displayOfficeSettings.display_fields})
