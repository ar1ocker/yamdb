from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import get_random_code
from .validators import username_validator


class ConfirmationCode(models.Model):
    code = models.TextField()
    user = models.OneToOneField('User', on_delete=models.CASCADE)


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        administrator = 'admin', 'Администратор'
        moderator = 'moderator', 'Модератор'
        user = 'user', 'Пользователь'

    username = models.TextField(max_length=150, unique=True,
                                validators=[username_validator])
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.TextField(choices=UserRoles.choices,
                            default=UserRoles.user)

    class Meta:
        ordering = ('-username', )

    def set_confirmation_code(self):
        code = get_random_code()

        obj, created = (ConfirmationCode
                        .objects
                        .get_or_create(user=self, defaults={'code': code}))

        if not created:  # Если код уже был - обновляем код
            obj.code = code
            obj.save()

        return code

    @property
    def is_user(self):
        return self.role == self.UserRoles.user

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.moderator

    @property
    def is_admin(self):
        return (self.role == self.UserRoles.administrator
                or self.is_superuser)
