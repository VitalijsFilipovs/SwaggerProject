from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка, является ли пользователь владельцем объекта
        return obj.owner == request.user

class IsLandlordOrReadOnly(BasePermission):
    """
    - landlord: может всё (CRUD) со своими объявлениями.
    - renter: только чтение.
    Применять на вьюсет объявлений.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        # разрешаем unsafe методы только арендодателю
        return hasattr(user, "profile") and user.profile.role == "landlord"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        # редактировать/удалять может только владелец-арендодатель
        return (
            hasattr(user, "profile") and user.profile.role == "landlord"
            and hasattr(obj, "owner") and obj.owner_id == user.id
        )