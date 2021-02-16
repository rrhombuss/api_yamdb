from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, ReviewViewSet, GenresViewSet, CategoryViewSet, CommentViewSet, UserViewSet, MyUserViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


router = DefaultRouter()
router.register(r'genres', GenresViewSet, basename='genres-list')
#router.register(r'users/(?P<username>\w+)', UsernameViewSet, basename='user-specific')

router.register(r'categories', CategoryViewSet, basename='comment-list')
router.register(r'titles', TitleViewSet, basename='titles-list')
router.register(r'reviews', ReviewViewSet, basename='review-list')
router.register(r'comments', CommentViewSet, basename='comments-list')
router.register(r'users/me', MyUserViewSet, basename='user-me')
router.register(r'users', UserViewSet, basename='user-all')



urlpatterns = [
    path('v1/auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/gettoken', views.get_token, name='gettoken'),
    #path('v1/auth/email', include(views.email_confirm)),
    path('v1/users/me', MyUserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='smth'),
    path('v1/', include(router.urls)),
    path('v1/titles/<int:title_id>/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/', include(router.urls)),
]
