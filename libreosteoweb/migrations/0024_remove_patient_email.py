# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0023_patient_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
    ]
