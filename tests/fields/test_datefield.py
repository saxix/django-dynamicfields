# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import pytest
from datetime import datetime
from django.utils import timezone

from django_dynamicfields.models import CustomFieldDefs
from django_dynamicfields.fields import DateField

from demoproject.models import DocumentField, DocumentTable

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("input", [DocumentField, DocumentTable])
@pytest.mark.django_db
def test_value(input):
    CustomFieldDefs.objects.add_to_model(input,
                                         name='custom',
                                         default_value=timezone.now,
                                         field_type=DateField)
    c1 = input(title='1')
    c1.dynamic.custom = datetime.today().date()
    c1.save()
    assert c1.dynamic.custom == datetime.today().date()
