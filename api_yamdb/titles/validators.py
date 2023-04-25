from datetime import datetime
from rest_framework.exceptions import ValidationError


def max_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError('Год не может быть больше текущего')
