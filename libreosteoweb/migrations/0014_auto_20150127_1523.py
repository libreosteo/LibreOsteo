# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0013_officesettings_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='office_address_city',
            field=models.CharField(default=b'', max_length=200, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='office_address_complement',
            field=models.CharField(default=b'', max_length=500, verbose_name='Address complement', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='office_address_street',
            field=models.CharField(default=b'', max_length=500, verbose_name='Street', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='office_address_zipcode',
            field=models.CharField(default=b'', max_length=200, verbose_name='Zipcode', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='office_phone',
            field=models.CharField(default=b'', max_length=200, verbose_name='Phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='officesettings',
            name='office_address_street',
            field=models.CharField(max_length=500, verbose_name='Street', blank=True),
        ),
    ]
