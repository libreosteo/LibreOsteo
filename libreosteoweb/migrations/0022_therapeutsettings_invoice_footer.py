# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0021_therapeutsettings_siret'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapeutsettings',
            name='invoice_footer',
            field=models.TextField(null=True, verbose_name='Invoice footer', blank=True),
            preserve_default=True,
        ),
    ]
