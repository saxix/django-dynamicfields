# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

# from .registry import *
from django.contrib.postgres import lookups
from django.contrib.postgres.fields.jsonb import KeyTransformFactory
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db.models import Field
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from psycopg2._json import Json

from django_dynamicfields.config import BAD_DATA_RAISE, BAD_DATA_SET_NONE, DYNAMIC_FIELDS
from django_dynamicfields.exceptions import DataValueError

from .exceptions import DrfValidationError
from .models import CustomFieldDefs
from .registry import *  # noqa

logger = logging.getLogger(__name__)


class FieldProxy(object):
    __slots = ('field', 'instance', 'data')

    def __init__(self, field, instance):
        self.field = field
        self.instance = instance
        # self.data = self.instance.__dict__[self.field.name] or {}
        super(FieldProxy, self).__init__()

    @cached_property
    def declared_fields(self):
        return CustomFieldDefs.objects.get_for_model(self.field.model)

    @cached_property
    def _all(self):
        return list(self.declared_fields.values_list('name', flat=True))

    @property
    def data(self):
        if not self.instance.__dict__[self.field.name]:
            self.instance.__dict__[self.field.name] = {}
        return self.instance.__dict__[self.field.name]

    def __setattr__(self, name, value):
        if name in self.__slots:
            super(FieldProxy, self).__setattr__(name, value)
        else:
            if name in self._all:
                f = self.declared_fields.get(name=name)
                f.validate(value)
                value = f.field.to_representation(value)
                self.data[name] = value
            else:
                raise FieldDoesNotExist("{} does not have custom field '{}'".format(self.field.model,
                                                                                    name))

    def __getattr__(self, name):
        if name in self._all:
            try:
                f = self.declared_fields.get(name=name)
                value = self.data[name]
                return f.field.to_internal_value(value)
            except DrfValidationError:
                if DYNAMIC_FIELDS['BAD_DATA_POLICY'] == BAD_DATA_RAISE:
                    raise DataValueError("{}.{}. {}".format(self.field.model,
                                                        name,
                                                        value))
                elif DYNAMIC_FIELDS['BAD_DATA_POLICY'] == BAD_DATA_SET_NONE:
                    return None

            except KeyError:
                return self.declared_fields.get(name=name).default_value
        raise FieldDoesNotExist("{} does not have custom field '{}'".format(self.field.model,
                                                                            name))


class ProxyFieldDescriptor(object):
    def __init__(self, field, proxy_class):
        self.field = field
        self.proxy_class = proxy_class

    def __get__(self, instance=None, owner=None):
        if not hasattr(instance, '_dynamic_field_proxy'):
            instance._dynamic_field_proxy = self.proxy_class(self.field, instance)
        return instance._dynamic_field_proxy
        # return self.proxy_class(self.field, instance)

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


# @deconstructible
# class DynamicFieldValidator(BaseValidator):
#     compare = lambda self, a, b: a > b
#     clean = lambda self, x: len(x)
#     message = ungettext_lazy(
#         'Ensure this value has at most %(limit_value)d character (it has %(show_value)d).',
#         'Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).',
#         'limit_value')
#     code = 'max_length'

class DynamicFieldManager(object):
    def __init__(self, model):
        self.model = model
        super(DynamicFieldManager, self).__init__()

    def extract_custom_fields(self, validated_data):
        copy = dict(validated_data)
        custom_values = {key: validated_data.pop(key) for (key, value)
                         in copy.viewitems()
                         if key in self._all}
        return validated_data, custom_values

    @property
    def _all(self):
        return list(self.declared_fields.values_list('name', flat=True))

    @property
    def declared_fields(self):
        return CustomFieldDefs.objects.get_for_model(self.model)


class DynamicField(Field):
    empty_strings_allowed = True
    description = _('A DynamicField object')

    def db_type(self, connection):
        return 'jsonb'

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['null'] = True
        kwargs['blank'] = True
        super(DynamicField, self).__init__(*args, **kwargs)
        # self.validators.append(DynamicFieldValidator)

    def validate_model(self, sender, instance, **kwargs):
        me = getattr(instance, self.name)
        stored = instance.__dict__[self.name] or {}
        # check mandatory fields
        for field in me.declared_fields:
            if field.mandatory and (not stored or field.name not in stored):
                raise ValidationError("{0.name} is required".format(self))

    def contribute_to_class(self, cls, name, **kwargs):
        super(DynamicField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, '_dynamicfield_holder', DynamicFieldManager(cls))
        setattr(cls, self.name, ProxyFieldDescriptor(self,
                                                     FieldProxy))

        from django.db.models.signals import pre_save
        pre_save.connect(self.validate_model,
                         sender=cls,
                         dispatch_uid='dynamicfield_pre_save')

    def get_db_prep_save(self, value, connection):
        return json.dumps(value.instance.__dict__[self.name])

    def get_transform(self, name):
        transform = super(DynamicField, self).get_transform(name)
        if transform:
            return transform
        return KeyTransformFactory(name)

    def to_python(self, value):
        return json.dumps(value.instance.__dict__[self.name])

    def get_prep_value(self, value):
        if value is not None:
            return Json(value)
        return value

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('has_key', 'has_keys', 'has_any_keys'):
            return value
        if isinstance(value, (dict, list)):
            return Json(value)
        return super(DynamicField, self).get_prep_lookup(lookup_type, value)

    def validate(self, value, model_instance):
        super(DynamicField, self).validate(value, model_instance)
        try:
            json.dumps(value)
        except TypeError:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return value

        # def formfield(self, **kwargs):
        #     defaults = {'form_class': forms.JSONField}
        #     defaults.update(kwargs)
        #     return super(DynamicField, self).formfield(**defaults)


DynamicField.register_lookup(lookups.DataContains)
DynamicField.register_lookup(lookups.ContainedBy)
DynamicField.register_lookup(lookups.HasKey)
DynamicField.register_lookup(lookups.HasKeys)
DynamicField.register_lookup(lookups.HasAnyKeys)
