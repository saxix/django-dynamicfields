# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django_dynamicfields.viewset import DynamicModelSerializerMixin
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import DocumentTable, DocumentField

logger = logging.getLogger(__name__)


class DocumentTableSerializer(DynamicModelSerializerMixin, ModelSerializer):
    class Meta:
        model = DocumentTable


class DocumentTableViewSet(ModelViewSet):
    serializer_class = DocumentTableSerializer
    queryset = DocumentTableSerializer.Meta.model.objects.all()


class DocumentFieldSerializer(DynamicModelSerializerMixin, ModelSerializer):
    class Meta:
        model = DocumentField
        # exclude = ('dynamic',)  # always exclude data storage


class DocumentFieldViewSet(ModelViewSet):
    serializer_class = DocumentFieldSerializer
    queryset = DocumentFieldSerializer.Meta.model.objects.all()


class DocumentFieldCreateView(CreateAPIView):
    serializer_class = DocumentFieldSerializer
    queryset = DocumentFieldSerializer.Meta.model.objects.all()


class DocumentTableCreateView(CreateAPIView):
    serializer_class = DocumentTableSerializer
    queryset = DocumentTableSerializer.Meta.model.objects.all()
