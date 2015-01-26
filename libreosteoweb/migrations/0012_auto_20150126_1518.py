# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0011_officesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapeutsettings',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
