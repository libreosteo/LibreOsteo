# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0010_auto_20150126_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_office_header', models.CharField(max_length=500, verbose_name='Invoice office header', blank=True)),
                ('office_address_street', models.CharField(max_length=500, verbose_name='street', blank=True)),
                ('office_address_complement', models.CharField(max_length=500, verbose_name='Address complement', blank=True)),
                ('office_address_zipcode', models.CharField(max_length=200, verbose_name='Zipcode', blank=True)),
                ('office_address_city', models.CharField(max_length=200, verbose_name='City', blank=True)),
                ('office_phone', models.CharField(max_length=200, verbose_name='Phone', blank=True)),
                ('office_siret', models.CharField(max_length=20, verbose_name='Siret')),
                ('currency', models.CharField(max_length=10, verbose_name='Currency')),
                ('invoice_content', models.TextField(verbose_name='Invoice content', blank=True)),
                ('invoice_footer', models.TextField(verbose_name='Invoice footer', blank=True)),
                ('invoice_start_sequence', models.TextField(verbose_name='Invoice start sequence', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
