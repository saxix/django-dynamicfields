# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django_dynamicfields.fields import DynamicField


class DocumentTable(models.Model):
    title = models.CharField(max_length=100)
    dynamic = DynamicField()

    class Meta:
        app_label = 'demoproject'

    def __unicode__(self):
        return self.title


class DocumentField(models.Model):
    title = models.CharField(max_length=100)
    dynamic = DynamicField()

    class Meta:
        app_label = 'demoproject'

    def __unicode__(self):
        return self.title


class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Document(models.Model):
    doc_type = models.ForeignKey(DocumentType)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
