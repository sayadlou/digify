import re

from django.core.exceptions import ValidationError


def is_valid_iran_code(value):
    if not re.search(r'^\d{10}$', value):
        raise ValidationError('Invalid Iranian National ID', code='invalid')
    check = int(value[9])
    s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11
    if s < 2:
        if not check == s:
            raise ValidationError('Invalid Iranian National ID', code='invalid')
    else:
        if not check + s == 11:
            raise ValidationError('Invalid Iranian National ID', code='invalid')


def is_valid_mobile_number(value):
    if not re.search(r'^\d{11}$', value):
        raise ValidationError('Invalid mobile number', code='invalid')
    if not value.startswith("09"):
        raise ValidationError('Invalid mobile number', code='invalid')
