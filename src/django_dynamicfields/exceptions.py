# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError as DrfValidationError  # noqa

logger = logging.getLogger(__name__)


class ValueNotFound(ObjectDoesNotExist):
    pass


class DataValueError(ValueError):
    pass
