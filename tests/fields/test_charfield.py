# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pytest
from django_dynamicfields.exceptions import ValidationError

from django_dynamicfields.models import CustomFieldDefs
from django_dynamicfields.fields import CharField

from demoproject.models import DocumentField, DocumentTable

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_max_length(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         init_string=json.dumps({'max_length': 1}),
                                         default_value='a',
                                         field_type=CharField)
    c1 = input(title='1')
    with pytest.raises(ValidationError):
        c1.dynamic.custom = 'abc'


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_min_length(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         init_string=json.dumps({'min_length': 10}),
                                         default_value='a',
                                         field_type=CharField)
    c1 = input(title='1')
    with pytest.raises(ValidationError):
        c1.dynamic.custom = 'abc'


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_mandatory(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         mandatory=True,
                                         field_type=CharField)
    c1 = input(title='1')
    with pytest.raises(ValidationError):
        c1.save()
