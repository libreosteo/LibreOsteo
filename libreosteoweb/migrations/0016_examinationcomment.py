# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libreosteoweb', '0015_auto_20150410_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExaminationComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(verbose_name='Comment')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('examination', models.ForeignKey(verbose_name='Examination', to='libreosteoweb.Examination')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
