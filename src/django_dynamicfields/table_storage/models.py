# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from picklefield import PickledObjectField

from django_dynamicfields.models import CustomFieldDefs

logger = logging.getLogger(__name__)


class DataStorageManager(models.Manager):
    def filter_for_model(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        return TableStorage.objects.filter(content_type=ct,
                                           object_id=instance.pk)

    def update_instance(self, instance, name, value):
        ct = ContentType.objects.get_for_model(instance)
        TableStorage.objects.update_or_create(
            content_type=ct,
            object_id=instance.pk,
            field=CustomFieldDefs.objects.get(name=name, content_type=ct),
            defaults={'value': value}
        )

    def get_for_instance(self, instance, name):
        try:
            ct = ContentType.objects.get_for_model(instance)
            attr = TableStorage.objects.get(content_type=ct,
                                            object_id=instance.pk,
                                            field__name=name)

            return attr.value
        except ObjectDoesNotExist:
            # raise ValueNotFound(name)
            raise AttributeError("'{}' object has no custom field '{}'".format(instance.__class__.__name__,
                                                                               name))


class TableStorage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field = models.ForeignKey(CustomFieldDefs)
    value = PickledObjectField()

    objects = DataStorageManager()

    def clear(self, instance):
        TableStorage.objects.filter_for_model(instance).delete()

    def store(self, instance, field, value):
        TableStorage.objects.update_instance(instance, field, value)

    def retrieve(self, instance, field):
        return TableStorage.objects.get_for_instance(instance, field)
