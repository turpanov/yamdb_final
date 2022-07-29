from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .validators import validate_score, validate_username, year_validator


class Users(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    user_roles = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, validate_username],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    role = models.CharField(
        _('Роль'),
        max_length=10,
        choices=user_roles,
        default=USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
        null=True
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        blank=True,
        null=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=10,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        db_index=True
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка категории'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(verbose_name='Жанр', db_index=True, max_length=256)
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Ссылка жанра', max_length=50
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Произведение'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[year_validator],
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения'
    )
    description = models.TextField(
        help_text='Описание',
        blank=True, null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
    )
    description = models.TextField(help_text='Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Rating(models.Model):
    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name='ratings',
        primary_key=True,
        verbose_name='Произведение'
    )
    ratings = models.PositiveSmallIntegerField(
        help_text='Средняя оценка',
        blank=True,
        verbose_name='Рейтинг'
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    title = models.ForeignKey(
        Title, related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст ревью'
    )
    author = models.ForeignKey(
        Users, related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор ревью'
    )
    score = models.PositiveSmallIntegerField(
        help_text='Оценка от 1 до 10',
        blank=True,
        validators=[validate_score],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Ревью'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        Users,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
