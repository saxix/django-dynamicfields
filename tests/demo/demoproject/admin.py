# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import DocumentField, DocumentTable, DocumentType, Document

admin.site.register([DocumentTable, DocumentField, DocumentType])


@admin.register(Document)
class IDocument(ModelAdmin):
    list_display = ('title', 'doc_type')
