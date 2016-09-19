# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from rest_framework import fields

logger = logging.getLogger(__name__)


class Storage(object):
    def __init__(self, *args, **kwargs):
        pass

    def clear(self, instance):
        pass

    def store(self, instance, field, value):
        pass

    def retrieve(self, instance, field):
        pass


class FieldStorage(Storage):
    def __init__(self, container, *args, **kwargs):
        self.container = container

    def clear(self, instance):
        setattr(instance, self.container, fields.empty)

    def store(self, instance, field, value):
        c = getattr(instance, self.container)
        if c:
            c[field] = value
        else:
            c = {field: value}
        setattr(instance, self.container, c)
        instance.save()

    def retrieve(self, instance, field):
        c = getattr(instance, self.container)
        if c:
            return c[field]
        return None
