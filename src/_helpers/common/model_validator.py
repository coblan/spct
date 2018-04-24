from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re

def int_str(value):
    if value and not re.match('^\d+$',value.strip()):
        raise ValidationError(
            _('%(value)s is not integer number'),
            params={'value': value},
        )

def has_str(value):
    if not value:
        raise ValidationError(
                    _('must input string'),
                )        