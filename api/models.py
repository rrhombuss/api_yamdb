from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('admin')
        MODERATOR = 'moderator', _('moderator')
        USER = 'user', _('user')

    role = models.CharField(
        verbose_name='роль',
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER,
    )

    @property
    def is_admin(self):
        return self.role in {
            self.Roles.ADMIN,
        }

    @property
    def is_moderator(self):
        return self.role in {
            self.Roles.MODERATOR,
        }

    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True,
                           verbose_name='биография')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', ]


class Genre(models.Model):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(max_length=200, verbose_name='Жанр', unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    """
    name = models.CharField(
        max_length=200, verbose_name='Категория', unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(
        validators=[MaxValueValidator(int(datetime.today().year)), ],
        null=True, verbose_name='Год издания', db_index=True
    )
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name='titles',
                                   null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles', blank=True)
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['id']


class Review(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews', null=True, blank=True)
    score = models.IntegerField(verbose_name='оценка')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ревью'


class Comment(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
