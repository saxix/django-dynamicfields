# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

BAD_DATA_SET_NONE = 1
BAD_DATA_RAISE = 2

DYNAMIC_FIELDS = {
    'BAD_DATA_POLICY': BAD_DATA_RAISE
}

DYNAMIC_FIELDS.update(getattr(settings, 'DYNAMIC_FIELDS', {}))
