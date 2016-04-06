# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0023_auto_20160312_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_patient', models.FileField(upload_to=b'', verbose_name='Patient file')),
                ('file_examination', models.FileField(upload_to=b'', verbose_name='Examination file', blank=True)),
            ],
        ),
    ]
