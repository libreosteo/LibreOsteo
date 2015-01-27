# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0012_auto_20150126_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='officesettings',
            name='amount',
            field=models.FloatField(default=None, null=True, verbose_name='Amount', blank=True),
            preserve_default=True,
        ),
    ]
