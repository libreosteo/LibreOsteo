# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-06 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0036_invoice_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='invoice',
        ),
        migrations.AddField(
            model_name='examination',
            name='invoices',
            field=models.ManyToManyField(blank=True, to='libreosteoweb.Invoice', verbose_name='Invoice'),
        ),
    ]