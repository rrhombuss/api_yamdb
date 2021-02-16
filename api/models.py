from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('moderator', 'moderator'),
        )
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_CHOICES[1][0], max_length=500)
    bio = models.CharField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=70)      
    year = models.DateField()
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='titles', blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='titles', null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    score = models.IntegerField()
    pub_date = models.DateTimeField()

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")


