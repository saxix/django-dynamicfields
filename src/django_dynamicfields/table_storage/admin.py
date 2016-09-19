# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import TableStorage


@admin.register(TableStorage)
class ICustomFieldHolder(ModelAdmin):
    list_display = ('field', 'value')
