# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0022_patient_current_treatment'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='laterality',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Laterality', choices=[(b'L', 'Left-handed'), (b'R', 'Right-handed')]),
        ),
    ]
