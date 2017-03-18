# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from vvcatalog.conf import CURRENCY


register = template.Library()

@register.simple_tag
def get_currency():
    return CURRENCY
