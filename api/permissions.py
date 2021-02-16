from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrSuperUser(BasePermission): 
    def has_object_permission(self, request, view, obj):
        return ( 
            request.method in SAFE_METHODS and request.user.is_authenticated or obj.author == request.user or request.user.role in ['admin', 'moderator',]
        ) 

class IsHimselfOrSuperUser(BasePermission): 
    def has_object_permission(self, request, view, obj):
        return ( 
            request.user.is_authenticated and obj.username == request.user.username or request.user.role in ['admin', 'moderator',]
        ) 

class IsAboveUser(BasePermission): 
    def has_permission(self, request, view):
            return bool(request.user.is_authenticated and request.user.role in ['admin', 'moderator',])

class IsAdmin(BasePermission): 
    def has_permission(self, request, view):
            return bool(request.user.is_authenticated and request.user.role in ['admin',])