# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0017_auto_20150415_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationcomment',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Date', blank=True),
        ),
    ]
