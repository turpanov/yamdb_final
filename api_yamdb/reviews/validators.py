from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_score(value):
    if value not in range(1, 11):
        raise ValidationError('Оценка может быть от 1 до 10')


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя пользователя не может быть - me')


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(f'{value} год еще не наступил!')
