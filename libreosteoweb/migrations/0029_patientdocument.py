# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0028_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDocument',
            fields=[
                ('attachment_type', models.SmallIntegerField(verbose_name='attachmentType')),
                ('document', models.OneToOneField(primary_key=True, serialize=False, to='libreosteoweb.Document', verbose_name='document')),
                ('patient', models.ForeignKey(verbose_name='patient', serialize=False, to='libreosteoweb.Patient'))
            ],
        ),
    ]
