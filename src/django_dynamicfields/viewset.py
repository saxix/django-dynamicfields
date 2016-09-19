# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import fields

from django_dynamicfields.fields import DynamicField
from django_dynamicfields.models import CustomFieldDefs

logger = logging.getLogger(__name__)


# class DynamicDestroyModelMixin(object):
#     def perform_destroy(self, instance):
#         instance.dyna.clear()
#         instance.delete()


class DynamicModelSerializerMixin(object):
    # def run_validation(self, data=fields.empty):
    #     for field in CustomField.objects.filter(content_type=ContentType.objects.get_for_model(self.Meta.model)):
    #         self.fields[field.name] = field.get_instance()
    #     return super(DynamicModelSerializerMixin, self).run_validation(data)

    def get_fields(self):
        ret = super(DynamicModelSerializerMixin, self).get_fields()
        ret = dict([(k, v) for k, v in ret.items() if
                    not (hasattr(v, 'model_field') and
                         isinstance(v.model_field, DynamicField))])
        for field in CustomFieldDefs.objects.filter(content_type=ContentType.objects.get_for_model(self.Meta.model)):
            ret[field.name] = field.field
        return ret

    def update(self, instance, validated_data):
        validated_data, custom_values = self.Meta.model._dynamicfield_holder.extract_custom_fields(validated_data)
        # self.Meta.model._dynamicfield_holder.store(instance, **custom_values)
        instance.dynamic = custom_values
        return super(DynamicModelSerializerMixin, self).update(instance, validated_data)

    def create(self, validated_data):
        validated_data, custom_values = self.Meta.model._dynamicfield_holder.extract_custom_fields(validated_data)
        instance = super(DynamicModelSerializerMixin, self).create(validated_data)
        instance.dynamic = custom_values
        instance.save()
        # self.Meta.model._dynamicfield_holder.store(instance, **custom_values)
        return instance


class ForeignKeyDynamicModelSerializerMixin(DynamicModelSerializerMixin):
    def run_validation(self, data=fields.empty):
        for field in CustomFieldDefs.objects.filter(content_type=ContentType.objects.get_for_model(self.Meta.model)):
            self.fields[field.name] = field.get_instance()
        return super(DynamicModelSerializerMixin, self).run_validation(data)
