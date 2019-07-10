# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def convert_all_new_line(apps, schema_editor):
	Patient = apps.get_model("libreosteoweb", "Patient")
	for patient in Patient.objects.all():
		patient.hobbies = patient.hobbies.replace('\n', '<br />')
		patient.important_info = patient.important_info.replace('\n', '<br />')
		patient.surgical_history = patient.surgical_history.replace('\n', '<br />')
		patient.medical_history = patient.medical_history.replace('\n', '<br />')
		patient.family_history = patient.family_history.replace('\n', '<br />')
		patient.trauma_history = patient.trauma_history.replace('\n', '<br />')
		patient.medical_reports = patient.medical_reports.replace('\n', '<br />')
		patient.save()

	Examination = apps.get_model("libreosteoweb", "Examination")
	for examination in Examination.objects.all():
		examination.reason_description = examination.reason_description.replace('\n', '<br />')
		examination.orl = examination.orl.replace('\n', '<br />')
		examination.visceral = examination.visceral.replace('\n', '<br />')
		examination.pulmo = examination.pulmo.replace('\n', '<br />')
		examination.uro_gyneco = examination.uro_gyneco.replace('\n', '<br />')
		examination.periphery = examination.periphery.replace('\n', '<br />')
		examination.general_state = examination.general_state.replace('\n', '<br />')
		examination.medical_examination = examination.medical_examination.replace('\n', '<br />')
		examination.diagnosis = examination.diagnosis.replace('\n', '<br />')
		examination.treatments = examination.treatments.replace('\n', '<br />')
		examination.conclusion = examination.conclusion.replace('\n', '<br />')
		examination.save()

from django.core.management import call_command


def rebuild_index(apps, schema_editor):
	try:
		call_command('clear_index', interactive=False)
		call_command('update_index', remove=True)
	except Exception :
		logger.error("Cannot rebuild index due to integrity model error.")

class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0021_update_name_in_app'),
    ]
    
    operations = [
        migrations.RunPython(convert_all_new_line),
    ]
    
