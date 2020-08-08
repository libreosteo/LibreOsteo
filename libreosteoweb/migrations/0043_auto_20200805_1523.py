# Generated by Django 2.2 on 2020-08-05 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libreosteoweb', '0042_auto_20200803_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='libreosteoweb.OfficeSettings', verbose_name='Office Settigns'),
        ),
        migrations.AddField(
            model_name='officesettings',
            name='office_name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Office name'),
        ),
    ]
