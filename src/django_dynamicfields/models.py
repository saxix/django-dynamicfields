# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import six
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from rest_framework.exceptions import ValidationError as DrfValidationError

from strategy_field.fields import StrategyClassField

from .registry import registry

logger = logging.getLogger(__name__)


class CustomFieldManager(models.Manager):
    def get_for_model(self, instance):
        return self.filter(content_type=ContentType.objects.get_for_model(instance))

    def add_to_model(self, Model, name, field_type, **kwargs):
        return self.create(content_type=ContentType.objects.get_for_model(Model),
                           name=name,
                           field_type=field_type,
                           **kwargs)


def validate_json(value):
    try:
        json.dumps(value)
    except TypeError:
        raise ValidationError(
            'Value must be valid JSON.',
            code='invalid',
            params={'value': value},
        )


class CustomFieldDefs(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    mandatory = models.BooleanField(default=False)
    field_type = StrategyClassField(registry=registry,
                                    display_attribute='label')
    init_string = models.CharField(max_length=1000, blank=True, null=True,
                                   validators=[validate_json])
    default_value = models.CharField(max_length=1000, blank=True, null=True)
    objects = CustomFieldManager()

    def validate(self, value):
        try:
            self.field.run_validators(value)
        except DrfValidationError as e:
            raise ValidationError(e)

    def clean(self):
        self._get_instance()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        super(CustomFieldDefs, self).save(force_insert, force_update, using, update_fields)

    def _get_instance(self):
        try:
            kwargs = {}
            if self.init_string:
                kwargs = json.loads(self.init_string)

            return self.field_type(required=self.mandatory,
                                   # default=self.default_value,
                                   label=self.name,
                                   **kwargs)
        except TypeError as e:
            msg = """Error creating DynamicField instance.
DynamicField record: #{r.pk} {r.name}
Field: {t}
Error: {e}""".format(t=self.field_type, e=str(e),
              r=self,)
            six.reraise(TypeError, msg)

    field = cached_property(_get_instance)
