# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0024_fileimport'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileimport',
            name='status',
            field=models.IntegerField(default=None, verbose_name='validity status', blank=True),
        ),
    ]
