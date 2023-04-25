import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Comment, Review
from titles.models import Category, Genre, GenreTitle, Title

User = get_user_model()

TABLES = [
    {'model': User,
     'file': 'users.csv',
     'integer_keys': ['id']},

    {'model': Category,
     'file': 'category.csv',
     'integer_keys': ['id']},

    {'model': Genre,
     'file': 'genre.csv',
     'integer_keys': ['id']},

    {'model': Title,
     'file': 'titles.csv',
     'integer_keys': ['id', 'category_id']},

    {'model': Review,
     'file': 'review.csv',
     'integer_keys': ['id', 'title_id', 'author_id']},

    {'model': Comment,
     'file': 'comments.csv',
     'integer_keys': ['id', 'review_id', 'author_id']},

    {'model': GenreTitle,
     'file': 'genre_title.csv',
     'integer_keys': ['id', 'title_id', 'genre_id']}
]


def try_to_int(value):
    try:
        return int(value)
    except ValueError:
        return value


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for csv_table in TABLES:
            model, file, integer_keys = csv_table.values()

            with open(settings.BASE_DIR / 'static/data' / file, 'r',
                      encoding='utf-8') as csv_file:

                reader = csv.DictReader(csv_file)

                data_for_load = []
                for data in reader:
                    for key in integer_keys:
                        data[key] = try_to_int(data[key])

                    data_for_load.append(model(**data))

                model.objects.bulk_create(data_for_load)

        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
