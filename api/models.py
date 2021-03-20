from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
 
    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
 
    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', ]


class Genre(models.Model):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(max_length=200, verbose_name="Жанр", unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    """
    name = models.CharField(
        max_length=200, verbose_name="Категория", unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(
        null=True, verbose_name="Год издания", db_index=True)
    description = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles",
                                   null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name="titles", blank=True)
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews', null=True, blank=True)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, 
                               related_name="comments")
