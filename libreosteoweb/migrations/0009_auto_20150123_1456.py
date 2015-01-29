# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0008_auto_20150123_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='therapeut_firstname',
            new_name='therapeut_first_name',
        ),
    ]
