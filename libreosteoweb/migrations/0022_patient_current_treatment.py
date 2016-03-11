# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0021_update_name_in_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='current_treatment',
            field=models.TextField(default=b'', verbose_name='Current treatment', blank=True),
        ),
    ]
