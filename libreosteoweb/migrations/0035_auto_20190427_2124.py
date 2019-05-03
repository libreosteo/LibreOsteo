# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-27 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0034_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='canceled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='libreosteoweb.Invoice', verbose_name='Canceled by'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_file',
            field=models.FileField(upload_to='documents', verbose_name='Document file'),
        ),
        migrations.AlterField(
            model_name='fileimport',
            name='file_examination',
            field=models.FileField(blank=True, upload_to='', verbose_name='Examination file'),
        ),
        migrations.AlterField(
            model_name='fileimport',
            name='file_patient',
            field=models.FileField(upload_to='', verbose_name='Patient file'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='office_address_city',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='office_address_complement',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Address complement'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='office_address_street',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='office_address_zipcode',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Zipcode'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='office_phone',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='current_treatment',
            field=models.TextField(blank=True, default='', verbose_name='Current treatment'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hobbies',
            field=models.TextField(blank=True, default='', verbose_name='Hobbies'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='job',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Job'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='laterality',
            field=models.CharField(blank=True, choices=[('L', 'Left-handed'), ('R', 'Right-handed')], max_length=1, null=True, verbose_name='Laterality'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, verbose_name='Sex'),
        ),
    ]