# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0026_auto_20160403_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version_string', models.CharField(max_length=15, null=True, verbose_name='Version', blank=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='patient',
            name='left_handedness',
            field=models.BooleanField(default=False, verbose_name='Left-handedness'),
            preserve_default=True,
        ),
    ]
