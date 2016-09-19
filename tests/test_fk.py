# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pytest
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django_dynamic_fixture import G
from rest_framework.test import APIClient
from strategy_field.utils import fqn

from django_dynamicfields.models import CustomFieldDefs
from django_dynamicfields.fields import BooleanField

from demoproject.api import DocumentFieldSerializer, DocumentTableSerializer
from demoproject.models import DocumentField, DocumentTable

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("input", [DocumentFieldSerializer, DocumentTableSerializer])
@pytest.mark.django_db
def test_base(input):
    model = input.Meta.model
    document = G(model)
    CustomFieldDefs.objects.add_to_model(model,
                                         name='preferred',
                                         field_type=fqn(BooleanField))
    ser = input(instance=document,
                data=model_to_dict(document))
    assert ser.is_valid(), ser._errors
    assert 'preferred' in ser.fields


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_create(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='preferred',
                                         field_type=fqn(BooleanField))

    url = reverse('api:{}-list'.format(input.__name__.lower()))
    client = APIClient()
    record = {'preferred': True,
              'title': 'Title'}
    res = client.post(url, record, format='json')
    record = json.loads(res.content)
    assert res.status_code == 201, res.status_code
    doc = input.objects.get(pk=record['id'])
    assert doc.dynamic.preferred


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_update(input):
    document = G(input)
    CustomFieldDefs.objects.add_to_model(input,
                                         name='preferred',
                                         field_type=fqn(BooleanField))

    url = reverse('api:{}-detail'.format(input.__name__.lower()), args=[document.pk])
    client = APIClient()
    res = client.get(url)
    # assert res.status_code == 200, res.json()
    record = res.json()
    record['preferred'] = True
    res = client.patch(url, record, format='json')

    assert res.status_code == 200, res.json()
    doc = input.objects.get(pk=record['id'])
    assert doc.dynamic.preferred


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_delete(input):
    document = G(input)

    CustomFieldDefs.objects.add_to_model(DocumentField,
                                         name='preferred',
                                         field_type=fqn(BooleanField))

    url = reverse('api:{}-detail'.format(input.__name__.lower()), args=[document.pk])
    client = APIClient()
    res = client.delete(url)

    assert res.status_code == 204, res
    with pytest.raises(input.DoesNotExist):
        document.refresh_from_db()
