# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0003_patient_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('clazz', models.TextField(verbose_name='Class', blank=True)),
                ('type', models.SmallIntegerField(verbose_name='Type')),
                ('comment', models.TextField(verbose_name='Comment', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='patient',
            name='creation_date',
            field=models.DateField(verbose_name='Creation date', null=True, editable=False, blank=True),
        ),
    ]
