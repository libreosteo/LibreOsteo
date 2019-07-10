# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libreosteoweb', '0023_patient_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_file', models.FileField(upload_to=b'documents', verbose_name='Document file')),
                ('title', models.TextField(verbose_name='Title')),
                ('notes', models.TextField(default=None, null=True, verbose_name='Notes', blank=True)),
                ('internal_date', models.DateTimeField(verbose_name='Adding date', blank=True)),
                ('document_date', models.DateField(default=None, null=True, verbose_name='Document date', blank=True)),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('mime_type', models.TextField(default=None, null=True, verbose_name='Mime-Type'))
            ],
        ),
    ]
