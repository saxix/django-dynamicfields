# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from strategy_field.utils import fqn

from django_dynamicfields.models import CustomFieldDefs
from django_dynamicfields.fields import BooleanField

from demoproject.models import DocumentField, DocumentTable

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_create(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='preferred',
                                         field_type=fqn(BooleanField))

    url = reverse('{}-create'.format(input.__name__.lower()))
    client = APIClient()
    record = {'preferred': True,
              'title': 'Title'}
    res = client.post(url, record, format='json')
    record = json.loads(res.content)
    assert res.status_code == 201, res.status_code
    doc = input.objects.get(pk=record['id'])
    assert doc.dynamic.preferred
