from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as views
from .views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet,
    MyTokenObtainPairView, ReviewViewSet,
    TitlesViewSet, UserViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register("titles", TitlesViewSet, basename='Title')
router.register("genres", GenreViewSet, basename='Genre')
router.register("categories", CategoryViewSet, basename='Category')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='Review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]

urlpatterns += [
    path('v1/auth/email/', views.mail_confirm, name='mail_confirm'),
    path(
        'v1/auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path("v1/token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
]
