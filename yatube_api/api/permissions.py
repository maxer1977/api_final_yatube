from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Предоставление прав на создание/редактирование/удаление.
    Авторизованный пользователь-владелец имеет полные права на
    свои записи. Аноним - только безопасные методы для списка.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """
    Предоставление прав просмотра записи любой категорией пользователей.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
