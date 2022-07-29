import math
import random
from statistics import mean

from django.core.mail import EmailMessage
from reviews.models import Review

from api_yamdb.settings import ADMIN_EMAIL


def generate_confirmation_code():
    symbols_for_code = "0123456789"
    code_lenght = 6
    confirmation_code = ""

    for _ in range(code_lenght):
        confirmation_code += symbols_for_code[math.floor(random.random() * 10)]

    return confirmation_code


def send_confirmation_code(confirmation_code, email):
    email = EmailMessage(
        'Код подтверждения для регистрации',
        f'Ваш код подтверждения для получения токена: {confirmation_code}',
        ADMIN_EMAIL,
        [email, ],
    )
    email.send()


def calculate_raiting(title_id):
    raiting_for_title = Review.objects.filter(title_id=title_id).values_list(
        'score', flat=True)
    return int(round(mean(raiting_for_title), 0))
