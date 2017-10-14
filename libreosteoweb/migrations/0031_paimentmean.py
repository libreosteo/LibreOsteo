# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0030_auto_20170917_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaimentMean',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('text', models.CharField(max_length=50, verbose_name='Text')),
            ],
        ),
        migrations.RunSQL("INSERT INTO libreosteoweb_paimentmean (code, text) VALUES ('check', 'Chèque');"),
        migrations.RunSQL("INSERT INTO libreosteoweb_paimentmean (code, text) VALUES ('cash', 'Espèce');"),
        migrations.RunSQL("INSERT INTO libreosteoweb_paimentmean (code, text) VALUES ('ecard', 'CB');")
    ]
