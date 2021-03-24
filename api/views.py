from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import SuspiciousOperation
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.filters import TitleFilter

from .models import Category, Genre, Title, User, Review
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrReadOnly)
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer,
                          ReviewOutSerializer,
                          CommentSerializer, MyTokenObtainPairSerializer)


class UpdateListViewSet(ListModelMixin,
                        UpdateModelMixin, GenericViewSet):
    pass


def mail_confirm(request):
    email_to = request.POST['email']
    if request.method == 'POST':
        user = User.objects.get_or_create(email=email_to, password=email_to)
        conf_code = default_token_generator._make_hash_value(user, 300)
        email = EmailMessage(
            'Conformation code',
            f'Your conformation code for authentification is {conf_code}.',
            email_to,
        )
        return email.send(fail_silently=False)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            return Response(UserSerializer(request.user).data)


class MyTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        if (
            ('email' in self.request.data)
            and ('confirmation_code' in self.request.data)
        ):
            return MyTokenObtainPairSerializer
        return TokenObtainPairSerializer


class TitlesViewSet(ModelViewSet):
    """
    Viewset который предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    """
    Вьюсет, обесечивающий `list()`, `create()`, `destroy()`
    """


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewOutSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if (
            int(self.request.data['score']) > 10
            or int(self.request.data['score']) < 1
            or Review.objects.filter(title=title, author=self.request.user)
        ):
            raise SuspiciousOperation("smths wrong coz i said so, lmao")
        else:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            serializer.save(title=title, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        elif (self.action == 'update' or self.action == 'partial_update'
              or self.action == 'destroy'):
            permission_classes = [IsAuthorOrReadOnly, ]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review, title=title, pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(
            Review, title=title, pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        elif (self.action == 'update' or self.action == 'partial_update'
              or self.action == 'destroy'):
            permission_classes = [IsAuthorOrReadOnly, ]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
