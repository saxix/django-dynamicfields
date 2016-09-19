# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import CustomFieldDefs


@admin.register(CustomFieldDefs)
class ICustomField(ModelAdmin):
    list_display = ('field_type', )
    # list_display = ('content_type', 'name', 'field_type', 'mandatory')
    search_fields = ('name',)
    list_filter = ('content_type', 'field_type', 'default_value')
