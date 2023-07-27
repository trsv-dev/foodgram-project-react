from rest_framework import permissions


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
