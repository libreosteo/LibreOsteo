# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from libreosteoweb.models import PaimentMean


def insert_default_paiment_mean(apps, schema_editor):
    for pm in [('check', 'Chèque', True), ('cash', 'Espèces', True),
               ('ecard', 'Carte Bancaire', False)]:
        pm_db = PaimentMean(code=pm[0], text=pm[1], enable=pm[2])
        pm_db.save()


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0030_auto_20170917_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaimentMean',
            fields=[
                ('id',
                 models.AutoField(verbose_name='ID',
                                  serialize=False,
                                  auto_created=True,
                                  primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('text', models.CharField(max_length=50, verbose_name='Text')),
                ('enable',
                 models.BooleanField(default=True, verbose_name='Enabled')),
            ],
        ),
        migrations.RunPython(insert_default_paiment_mean)
    ]
