# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libreosteoweb', '0004_auto_20141231_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='officeevent',
            name='reference',
            field=models.IntegerField(default=-1, verbose_name='Reference', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='officeevent',
            name='user',
            field=models.ForeignKey(default=0, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='officeevent',
            name='date',
            field=models.DateTimeField(verbose_name='Date', blank=True),
        ),
    ]
