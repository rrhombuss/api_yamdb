from rest_framework import serializers, status
from rest_framework.response import Response
from django.db.models import Avg
from .models import Category, Comment, Genre, Review, Title, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'name', 'slug'
        model = Category

class TitleSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format="%Y", input_formats=['%Y', 'iso-8601'])
    category = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        many = True,
        slug_field='name',
        read_only=True
    )
    #rating = serializers.SerializerMethodField()
    class Meta:
        fields = 'id', 'name', 'year', 'genre', 'category', 'description'
        model = Title

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        return int(reviews.rating_set.aggregate(Avg('score')).values()[0])

class TitleOutSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format="%Y", input_formats=['%Y', 'iso-8601'])
    genre = serializers.SlugRelatedField(
        many = True,
        slug_field='name',
        read_only=True
    )
    #rating = serializers.SerializerMethodField()
    class Meta:
        fields = 'id', 'name', 'year', 'genre', 'category', 'description'
        model = Title

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        return int(reviews.rating_set.aggregate(Avg('score')).values()[0])



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    
    class Meta:
        fields = '__all__'
        model = Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        lookup_field = 'username'
        #extra_kwargs = {'user': {'required': False}}