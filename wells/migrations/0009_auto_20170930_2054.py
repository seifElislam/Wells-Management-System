# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-30 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0008_auto_20170930_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]
