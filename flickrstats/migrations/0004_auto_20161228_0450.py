# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 04:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flickrstats', '0003_auto_20161228_0421'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daystatistic',
            old_name='ts_start',
            new_name='ts',
        ),
        migrations.RemoveField(
            model_name='daystatistic',
            name='ts_end',
        ),
        migrations.AlterField(
            model_name='daystatistic',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
