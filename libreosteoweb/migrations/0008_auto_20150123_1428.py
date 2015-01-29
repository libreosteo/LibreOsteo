# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0007_auto_20150123_0851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='patient_riginal_name',
            new_name='patient_original_name',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='therapeut_firstname',
            field=models.TextField(verbose_name='Therapeut firstname'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='therapeut_name',
            field=models.TextField(verbose_name='Therapeut name'),
        ),
    ]
