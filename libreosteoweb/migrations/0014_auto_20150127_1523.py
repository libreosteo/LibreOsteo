# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def init_settings(apps, schema_editor):
    # We can't import the Patient model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    OfficeSettings = apps.get_model("libreosteoweb", "OfficeSettings")
    if len(OfficeSettings.objects.all()) <= 0:
        officesettings = OfficeSettings()
        officesettings.invoice_office_header = ''
        officesettings.office_address_street = ''
        officesettings.office_address_complement = ''
        officesettings.office_address_zipcode = ''
        officesettings.office_address_city = ''
        officesettings.office_phone = ''
        officesettings.office_siret = ''
        officesettings.currency = ''
        officesettings.invoice_content = ''
        officesettings.invoice_footer = ''
        officesettings.invoice_start_sequence = ''
        officesettings.save()

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
        migrations.RunPython(init_settings),
    ]
