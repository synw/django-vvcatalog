# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

USE_PRICES = getattr(settings, 'SYMPA_USE_PRICES', True)
CURRENCY = getattr(settings, 'SYMPA_CURRENCY', '$')
PRICES_AS_INTEGER = getattr(settings, 'SYMPA_PRICES_AS_INTEGER', False)

CODE_MODE = getattr(settings, 'SYMPA_CODE_MODE', False)

default_statuses =  [
                     ("pending", _(u'Pending')),
                     ("published", _(u'Published')),
                     ("unpublished", _(u'Unpublished')),
                     ]

STATUSES = getattr(settings, 'MBASE_STATUSES', default_statuses)

CIVILITIES = (
      ('mr', _(u'Mr')),
      ('mm', _(u'Mme')),
)
