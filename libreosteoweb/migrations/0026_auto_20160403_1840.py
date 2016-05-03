# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0025_fileimport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileimport',
            name='status',
            field=models.IntegerField(default=None, null=True, verbose_name='validity status', blank=True),
        ),
    ]
