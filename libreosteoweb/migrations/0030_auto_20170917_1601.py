# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0029_patientdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdocument',
            name='patient',
            field=models.ForeignKey(verbose_name='patient', to='libreosteoweb.Patient'),
        ),
    ]
