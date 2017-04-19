# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

USE_PRICES = getattr(settings, 'VVCATALOG_USE_PRICES', True)
CURRENCY = getattr(settings, 'VVCATALOG_CURRENCY', '$')
PRICES_AS_INTEGER = getattr(settings, 'VVCATALOG_PRICES_AS_INTEGER', False)

CODE_MODE = getattr(settings, 'VVCATALOG_CODE_MODE', False)

PAGINATION = getattr(settings, 'VVCATALOG_PAGINATION', 10)

default_statuses =  [
                     ("pending", _(u'Pending')),
                     ("published", _(u'Published')),
                     ("unpublished", _(u'Unpublished')),
                     ]

STATUSES = getattr(settings, 'VV_STATUSES', default_statuses)

CIVILITIES = (
      ('mr', _(u'Mr')),
      ('mm', _(u'Mme')),
)

ORDER_STATUSES = (
                  ('pending', _(u'Pending')),
                  ('confirmed', _(u'Confirmed')),
                  ('closed', _(u'Closed')),
                  ('rejected', _(u'Rejected')),
                  )

ORDER_STATUSES = getattr(settings, 'VVCATALOG_STATUSES', ORDER_STATUSES)
