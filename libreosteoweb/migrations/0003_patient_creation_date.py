# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import date


def creation_date(apps, schema_editor):
    # We can't import the Patient model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Patient = apps.get_model("libreosteoweb", "Patient")
    for patient in Patient.objects.all():
        patient.creation_date = date(1970, 1, 1)
        patient.save()

class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0002_remove_examination_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='creation_date',
            field=models.DateField(null=True, verbose_name='Creation date', blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(creation_date),
    ]
