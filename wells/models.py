# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Field(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)


class OperationName(models.Model):
    name = models.CharField(max_length=50)


class OperationPerformance(models.Model):
    remarks = models.CharField(max_length=100)
    gross = models.FloatField(default=0.0)
    net = models.FloatField(default=0.0)
    gor = models.FloatField(default=0.0)
    dfl = models.FloatField(default=0.0)
    liq = models.FloatField(default=0.0)
    wc = models.FloatField(default=0.0)
    sep_p = models.IntegerField(default=0)


class Operation(models.Model):
    description = models.CharField(max_length=200)
    sketch = models.ImageField(upload_to='workover_sketch', blank=True, null=True)
    operation = models.ForeignKey(OperationName)
    user = models.ForeignKey(User)
    date = models.DateField("Date", default=date.today)
    performance = models.ForeignKey(OperationPerformance, null=True)


class Schedule(models.Model):
    date = models.CharField(max_length=10)
    field = models.ForeignKey(Field, default=1)


class Pump(models.Model):
    pump_type = models.CharField(max_length=50)
    pump_depth = models.FloatField(default=0.0)
    config = models.CharField(max_length=50)


class Well(models.Model):
    STATUS = (('N', 'Natural flow'), ('F', 'Artificial lift'), ('J', 'Injection'))
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    field = models.ForeignKey(Field)
    normal_value = models.FloatField(default=0.0)
    statues = models.CharField(max_length=1, choices=STATUS, default='N')
    operations = models.ManyToManyField(Operation)
    schedule_id = models.ManyToManyField(Schedule, related_name='regular_schedule')
    check_id = models.ManyToManyField(Schedule, related_name='check_schedule', null=True)
    pump = models.ForeignKey(Pump)
    need_check = models.BooleanField(default=False)


class WaterCut(models.Model):
    user = models.ForeignKey(User)
    value = models.FloatField(default=0.0)
    well = models.ForeignKey(Well)
    date = models.DateField("Date", default=date.today)


