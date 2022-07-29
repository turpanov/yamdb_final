import csv
import os

from django.core.management.base import BaseCommand
from django.db.models import Avg, IntegerField
from reviews.models import (Category, Comment, Genre, GenreTitle, Rating,
                            Review, Title, Users)

from api_yamdb.settings import BASE_DIR

path_to_data = 'static/data/'

TABLES = {
    Users: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                os.path.join(BASE_DIR, path_to_data, csv_f),
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        ratings = Review.objects.all().values('title_id').annotate(ratings=Avg(
            'score', output_field=IntegerField()))
        Rating.objects.bulk_create(Rating(**rating) for rating in ratings)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
