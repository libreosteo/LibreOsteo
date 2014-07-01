from django.shortcuts import render_to_response
from django.forms.models import ModelForm
from libreosteoweb.models import Patient, Children, RegularDoctor


def filter_fields(f):
    return f is not None and f.formfield() is not None

class PatientDisplay(ModelForm):
    class Meta:
        model = Patient

    display_fields = dict([ (f.name, f.formfield().label) for f in filter( filter_fields, Patient._meta.fields)])


def display_patient(request):
    display = PatientDisplay()
    return render_to_response('partials/patient-detail.html', {'patient' : display.display_fields})