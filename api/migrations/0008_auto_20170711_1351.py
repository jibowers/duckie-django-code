# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170711_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duckling',
            name='minute_frequency',
            field=models.IntegerField(blank=True, default=1440),
        ),
    ]
