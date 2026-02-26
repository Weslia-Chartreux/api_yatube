from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # безопасные методы (GET, HEAD, OPTIONS) — разрешаем всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # на изменение/удаление — только автор
        return obj.author == request.user