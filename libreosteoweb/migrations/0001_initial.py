# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family_name', models.CharField(max_length=200, verbose_name='Family name', blank=True)),
                ('first_name', models.CharField(max_length=200, verbose_name='Firstname')),
                ('birthday_date', models.DateField(verbose_name='Birth date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.TextField(verbose_name='Reason', blank=True)),
                ('reason_description', models.TextField(verbose_name='Reason description', blank=True)),
                ('orl', models.TextField(verbose_name='ORL Sphere', blank=True)),
                ('visceral', models.TextField(verbose_name='Visceral Sphere', blank=True)),
                ('pulmo', models.TextField(verbose_name='Cardio-Pulmo Sphere', blank=True)),
                ('uro_gyneco', models.TextField(verbose_name='Uro-gyneco Sphere', blank=True)),
                ('periphery', models.TextField(verbose_name='Periphery Sphere', blank=True)),
                ('general_state', models.TextField(verbose_name='General state', blank=True)),
                ('medical_examination', models.TextField(verbose_name='Medical examination', blank=True)),
                ('tests', models.TextField(verbose_name='Tests', blank=True)),
                ('diagnosis', models.TextField(verbose_name='Diagnosis', blank=True)),
                ('treatments', models.TextField(verbose_name='Treatments', blank=True)),
                ('conclusion', models.TextField(verbose_name='Conclusion', blank=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('status', models.SmallIntegerField(verbose_name='Status')),
                ('type', models.SmallIntegerField(verbose_name='Type')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family_name', models.CharField(max_length=200, verbose_name='Family name')),
                ('original_name', models.CharField(max_length=200, verbose_name='Original name', blank=True)),
                ('first_name', models.CharField(max_length=200, verbose_name='Firstname', blank=True)),
                ('birth_date', models.DateField(verbose_name='Birth date')),
                ('address_street', models.CharField(max_length=500, verbose_name='Street', blank=True)),
                ('address_complement', models.CharField(max_length=500, verbose_name='Address complement', blank=True)),
                ('address_zipcode', models.CharField(max_length=200, verbose_name='Zipcode', blank=True)),
                ('address_city', models.CharField(max_length=200, verbose_name='City', blank=True)),
                ('phone', models.CharField(max_length=200, verbose_name='Phone', blank=True)),
                ('mobile_phone', models.CharField(max_length=200, verbose_name='Mobile phone', blank=True)),
                ('smoker', models.BooleanField(default=False, verbose_name='Smoker')),
                ('important_info', models.TextField(verbose_name='Important note', blank=True)),
                ('surgical_history', models.TextField(verbose_name='Surgical history', blank=True)),
                ('medical_history', models.TextField(verbose_name='Medical history', blank=True)),
                ('family_history', models.TextField(verbose_name='Family history', blank=True)),
                ('trauma_history', models.TextField(verbose_name='Trauma history', blank=True)),
                ('medical_reports', models.TextField(verbose_name='Medical reports', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegularDoctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family_name', models.CharField(max_length=200, verbose_name='Family name')),
                ('first_name', models.CharField(max_length=200, verbose_name='Firstname')),
                ('phone', models.CharField(max_length=100, verbose_name='Phone', blank=True)),
                ('city', models.CharField(max_length=200, verbose_name='City', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(verbose_name='Regular doctor', blank=True, to='libreosteoweb.RegularDoctor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examination',
            name='patient',
            field=models.ForeignKey(verbose_name='Patient', to='libreosteoweb.Patient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examination',
            name='therapeut',
            field=models.ForeignKey(verbose_name='Therapeut', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='children',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', to='libreosteoweb.Patient'),
            preserve_default=True,
        ),
    ]
