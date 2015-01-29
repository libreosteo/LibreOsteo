# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0005_auto_20150105_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='status_reason',
            field=models.TextField(null=True, verbose_name='Status reason', blank=True),
            preserve_default=True,
        ),
    ]
