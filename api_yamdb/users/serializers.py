from django.conf import settings
from rest_framework import serializers

from .validators import username_validator


class UserSignupSerializer(serializers.Serializer):
    username = serializers.SlugField(
        max_length=150
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, value):
        username_validator(value)
        return value


class UserGetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )
    username = serializers.SlugField(
        max_length=150
    )
