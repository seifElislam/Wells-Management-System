# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

admin.site.register(Well)
admin.site.register(Field)
admin.site.register(Pump)
admin.site.register(OperationPerformance)
admin.site.register(Operation)
admin.site.register(OperationName)
admin.site.register(WaterCut)
admin.site.register(Schedule)


