from random import randint

from django.core.mail import EmailMessage
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict

from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin, ListModelMixin

from .permissions import IsAuthorOrSuperUser, IsAboveUser, IsAdmin, IsHimselfOrSuperUser
from .pages import CustomPagination
from .models import User, Review, Comment, Title, Genre, Category
from .serializers import ReviewSerializer, CategorySerializer, CommentSerializer, TitleSerializer, GenreSerializer, UserSerializer, TitleOutSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

def email_confirm(request):
    global random_code
    global email_to
    random_code = randint(1000, 9999)
    email_to = request.POST['email']
    email = EmailMessage(
        'bruv',
        f'ya code is {random_code}',
        'maks.pavlogradskiy.96@mail.ru',
        email_to
    )
    return email.send(fail_silently=False)

def get_token(request):
    # if request.POST['confirmation_code'] == random_code:
    email = request.POST['email']
    if not User.objects.filter(email=email).exists():
        if request.method == 'POST':
            username = email.split('@')[0]
            user = User.objects.create(username=username, email=email)
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                
            }, status=status.HTTP_200_OK)
                    
        
    return Response(['this user already exists']).json()
# return Response(['incorrect code']).json()  

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_permissions(self):
        if self.action == 'create' or self.action == 'perform_create':
            permission_classes = [IsHimselfOrSuperUser]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]

        # elif self.action == 'list':
        #     permission_classes = [IsAboveUser]
        elif self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class MyUserViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):

        return User.objects.filter(username=self.request.user.username)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset[0])
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        queryset = self.list()
        serializer = UserSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        
    # def get_permissions(self):
    #     if self.action == 'create' or self.action == 'perform_create':
    #         permission_classes = []
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]
    #     return [permission() for permission in permission_classes]

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all() 
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        category = get_object_or_404(Category, slug=self.request.POST['category'])
        print(category.name)
        print(category.name)
        
        print(category.name)
        print(category.name)
        # print(category.first().name)
        # print(category.first().slug)
        # print(category.last().name)
        genre = self.request.POST['genre']
        # print(genre.first())
        # print(self.request.POST['genre'])
        # print(Genre.objects.filter(slug=self.request.POST['genre'][0]))
        author = self.request.user
        serializer.save(author=author, category=category)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = TitleOutSerializer
    #     # return Response(serializer.data)

    #     data = self.get_queryset()

    #     for item in data:
    #         item['category '] = model_to_dict(item['category'])

    #         return HttpResponse(json.simplejson.dumps(data), mimetype="application/json")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        title = get_object_or_404(Title, pk=slef.kwargs.get('title_id'))
        return title.reviews.all()

    def get_permissions(self):
        if self.action == 'create' or self.action == 'perform_create':
            permission_classes = [permissions.IsAuthenticated,]
        else:
            permission_classes = [IsAuthorOrSuperUser,]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        if self.action == 'create' or self.action == 'perform_create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'delete':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('title_id'))
        return review.comments.all()

class GenresViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated,]
        return [permission() for permission in permission_classes]




