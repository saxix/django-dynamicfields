# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import pytest
from django.core.exceptions import FieldDoesNotExist

from django_dynamicfields.models import CustomFieldDefs
from django_dynamicfields.fields import CharField

from demoproject.models import DocumentField, DocumentTable

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_base(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         default_value='a',
                                         field_type=CharField)
    c1 = input(title='1')
    assert c1.dynamic.custom == 'a'
    with pytest.raises(FieldDoesNotExist):
        assert c1.dynamic.wrong == 'a'


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_save(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         default_value='xx',
                                         field_type=CharField)
    c1 = input(title='1')
    c1.dynamic.custom = 'a'
    c1.save()
    assert c1.dynamic.custom == 'a'


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_save_default(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         default_value='def',
                                         field_type=CharField)
    c1 = input(title='1')
    c1.save()
    assert c1.dynamic.custom == 'def'


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_validate_value(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         default_value='def',
                                         field_type=CharField)
    c1 = input(title='1')
    c1.save()
    assert c1.dynamic.custom == 'def'
