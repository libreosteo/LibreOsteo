from django.shortcuts import render_to_response
from django.forms.models import ModelForm
from libreosteoweb.models import Patient, Children, RegularDoctor, Examination


def filter_fields(f):
    return f is not None and f.formfield() is not None

class PatientDisplay(ModelForm):
    class Meta:
        model = Patient

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, Patient._meta.fields)])

class RegularDoctorDisplay(ModelForm):
    class Meta:
        model = RegularDoctor

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, RegularDoctor._meta.fields)])

class ExaminationDisplay(ModelForm):
    class Meta:
        model = Examination

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, Examination._meta.fields)])

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

