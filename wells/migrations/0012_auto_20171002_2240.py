# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0011_auto_20171002_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='check_id',
            field=models.ManyToManyField(null=True, related_name='check_schedule', to='wells.Schedule'),
        ),
    ]
