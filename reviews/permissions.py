from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReviewOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # читать можно всем; создавать и менять — только аутентифицированным
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # редактировать/удалять — только автор отзыва
        return obj.user_id == request.user.id
