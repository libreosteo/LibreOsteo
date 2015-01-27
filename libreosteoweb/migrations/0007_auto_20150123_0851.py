# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0006_examination_status_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('currency', models.CharField(max_length=10, verbose_name='Currency')),
                ('paiment_mode', models.CharField(max_length=10, verbose_name='Paiment mode')),
                ('header', models.TextField(verbose_name='Header', blank=True)),
                ('therapeut_name', models.TextField(verbose_name='Therapeut')),
                ('therapeut_firstname', models.TextField(verbose_name='Therapeut')),
                ('quality', models.TextField(verbose_name='Quality')),
                ('adeli', models.TextField(verbose_name='Adeli')),
                ('location', models.TextField(verbose_name='Location')),
                ('number', models.TextField(verbose_name='Number')),
                ('patient_family_name', models.CharField(max_length=200, verbose_name='Family name')),
                ('patient_riginal_name', models.CharField(max_length=200, verbose_name='Original name', blank=True)),
                ('patient_first_name', models.CharField(max_length=200, verbose_name='Firstname', blank=True)),
                ('patient_address_street', models.CharField(max_length=500, verbose_name='Street', blank=True)),
                ('patient_address_complement', models.CharField(max_length=500, verbose_name='Address complement', blank=True)),
                ('patient_address_zipcode', models.CharField(max_length=200, verbose_name='Zipcode', blank=True)),
                ('patient_address_city', models.CharField(max_length=200, verbose_name='City', blank=True)),
                ('content_invoice', models.TextField(verbose_name='Content', blank=True)),
                ('footer', models.TextField(verbose_name='Footer', blank=True)),
                ('office_siret', models.TextField(verbose_name='Siret', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='examination',
            name='invoice',
            field=models.OneToOneField(null=True, blank=True, to='libreosteoweb.Invoice', verbose_name='Invoice'),
            preserve_default=True,
        ),
    ]
