# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170710_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='duckling',
            name='minute_frequency',
            field=models.IntegerField(default=1440),
        ),
        migrations.AddField(
            model_name='duckling',
            name='preferred_time',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='duckling',
            name='notification_schedule',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_q.Schedule'),
        ),
    ]
