# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-26 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='field',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wells.Field'),
        ),
    ]
