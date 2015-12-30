# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0019_auto_20150420_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Sex', choices=[(b'M', 'Male'), (b'F', 'Female')]),
            preserve_default=True,
        ),
    ]
