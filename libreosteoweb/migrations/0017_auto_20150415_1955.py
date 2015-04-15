# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0016_examinationcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationcomment',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Date'),
        ),
    ]
