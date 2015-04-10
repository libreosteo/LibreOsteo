# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0014_auto_20150127_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='hobbies',
            field=models.TextField(default=b'', verbose_name='Hobbies', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='job',
            field=models.CharField(default=b'', max_length=200, verbose_name='Job', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examination',
            name='reason_description',
            field=models.TextField(verbose_name='Reason description/Context', blank=True),
        ),
    ]
