from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or bool(request.user.is_admin)
        )


class AuthorModerAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_moderator
            or request.user.is_admin
            or request.user == obj.author)
