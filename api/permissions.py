from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.is_superuser)
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_authenticated
            and obj.username == request.user.username
        ):
            return True
        return (request.user.is_authenticated and request.user.is_superuser
                or request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    """
    Редактирование объекта возможно только для Администратора.
    Для чтения доступно всем.
    """
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and request.user.is_superuser
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and request.user.is_superuser
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_moderator:
            return True
        if request.method == 'PATCH' or request.method == 'DELETE':
            if obj.author == request.user:
                return True
        if request.user.is_authenticated and request.user.is_superuser:
            return True
