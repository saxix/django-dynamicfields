# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import fields

from strategy_field.registry import Registry
from strategy_field.utils import fqn

logger = logging.getLogger(__name__)

__all__ = ['BooleanField',
           'CharField',
           'DateField',
           'DateTimeField',
           'DecimalField',
           'EmailField',
           'IntegerField',
           'RegexField']


class DynamicMixin(object):
    def get_attribute(self, instance):
        try:
            super(DynamicMixin, self).get_attribute(instance)
        except AttributeError:
            try:
                return instance._dynamicfield_holder.retrieve(instance,
                                                              self.source_attrs[0])
            except ObjectDoesNotExist:
                return fields.empty


class FieldRegistry(Registry):
    def append(self, x):
        wrapper = type(x.__name__, (DynamicMixin, x), {})

        return super(FieldRegistry, self).append(wrapper)

    register = append


def customize(klass):
    return type(klass.__name__, (DynamicMixin, klass), {'label': classmethod(lambda s: fqn(s).split('.')[-1])})


BooleanField = customize(fields.BooleanField)
CharField = customize(fields.CharField)
DateField = customize(fields.DateField)
DateTimeField = customize(fields.DateTimeField)
DecimalField = customize(fields.DecimalField)
EmailField = customize(fields.EmailField)
IntegerField = customize(fields.IntegerField)
RegexField = customize(fields.RegexField)

registry = Registry(fields.Field)

registry.register(CharField)
registry.register(IntegerField)
registry.register(DateField)
registry.register(DateTimeField)
registry.register(EmailField)
registry.register(RegexField)
# registry.register(IPAddressField)
registry.register(DecimalField)
# registry.register(TimeField)
# registry.register(DurationField)
# registry.register(ChoiceField)
# registry.register(MultipleChoiceField)
# registry.register(FilePathField)
registry.register(BooleanField)
