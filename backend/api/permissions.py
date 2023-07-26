from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """Пермишн для анонимного пользователя."""

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous
        )


class IsAuthenticated(permissions.BasePermission):
    """Пермишн для авторизованного пользователя."""

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_superuser
        )


class IsAuthor(permissions.BasePermission):
    """Пермишн автора объекта."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """
    Пермишн для админа (включая суперюзера).
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser)
                )
        )
