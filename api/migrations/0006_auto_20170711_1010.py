# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 10:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170711_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duckling',
            name='notification_schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_q.Schedule'),
        ),
        migrations.AlterField(
            model_name='duckling',
            name='preferred_time',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
    ]
