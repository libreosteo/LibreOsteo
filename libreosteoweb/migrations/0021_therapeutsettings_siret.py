# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0026_auto_20160403_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapeutsettings',
            name='siret',
            field=models.CharField(max_length=20, null=True, verbose_name='Siret', blank=True),
            preserve_default=True,
        ),
    ]
