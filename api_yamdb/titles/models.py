from django.contrib.auth import get_user_model
from django.db import models

from .validators import max_year_validator

User = get_user_model()


class NameSlugMixin(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        ordering = ('-name', )

    def __str__(self):
        return self.name


class Category(NameSlugMixin):
    class Meta(NameSlugMixin.Meta):
        verbose_name = 'Категория'


class Genre(NameSlugMixin):
    class Meta(NameSlugMixin.Meta):
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(
        validators=[max_year_validator]
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        max_length=400,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр',
        through='GenreTitle'
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('-name', )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Связь M2M между произведениями и жанром
    Описана вручную для более простого импортирования
    тестовых данных
    """
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = 'Произведение и жанр'

    def __str__(self):
        return f'{self.title} {self.genre}'
