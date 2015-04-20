# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0018_auto_20150420_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulardoctor',
            name='phone',
            field=models.CharField(max_length=100, null=True, verbose_name='Phone', blank=True),
        ),
    ]
