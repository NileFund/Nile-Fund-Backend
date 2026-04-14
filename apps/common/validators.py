import re
from django.core.exceptions import ValidationError
from django.utils import timezone


PHONE_REGEX = r'^01[0125]\d{8}$'


def validate_egyptian_phone(value):
    if not re.fullmatch(PHONE_REGEX, value):
        raise ValidationError(
            ('Enter a valid Egyptian mobile number '
              '(010 / 011 / 012 / 015 followed by 8 digits).')
        )


def validate_not_in_past(value):
    if value < timezone.now():
        raise ValidationError('Start time cannot be in the past.')


def validate_future_date(value):
    if value <= timezone.now():
        raise ValidationError('End time must be in the future.')