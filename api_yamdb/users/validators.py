import re

from rest_framework import serializers


def username_validator(value):
    if value.lower() == 'me':
        raise serializers.ValidationError(
            {'username': 'Username "me" недоступен'}
        )
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise serializers.ValidationError(
            {'username': 'Значение должно состоять только из букв, '
                'цифр, символов подчёркивания, дефисов, знаков + и @'}
        )
