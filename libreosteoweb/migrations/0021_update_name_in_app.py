# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from libreosteoweb.api.filter import get_name_filters

def update_family_name(apps, schema_editor):
	filter_chain = get_name_filters()

	RegularDoctor = apps.get_model('libreosteoweb', 'RegularDoctor')
	for doctor in RegularDoctor.objects.all():
		doctor.family_name = filter_chain.filter(doctor.family_name)
		doctor.first_name = filter_chain.filter(doctor.first_name)
		doctor.save()

	Patient = apps.get_model('libreosteoweb', 'Patient')
	for patient in Patient.objects.all():
		patient.family_name = filter_chain.filter(patient.family_name)
		patient.first_name = filter_chain.filter(patient.first_name)
		patient.original_name = filter_chain.filter(patient.original_name)
		patient.save()

	Children = apps.get_model('libreosteoweb', 'Children')
	for children in Children.objects.all():
		children.family_name = filter_chain.filter(children.family_name)
		children.first_name = filter_chain.filter(children.first_name)
		children.save()

class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0027_auto_20160422_1540'),
    ]

    operations = [
    	migrations.RunPython(update_family_name),
    ]
