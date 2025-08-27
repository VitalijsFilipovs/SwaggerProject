from rest_framework.permissions import BasePermission, SAFE_METHODS

class BookingAccessPermission(BasePermission):
    """
    Правила:
    - Любой аутентифицированный может видеть свои бронирования.
    - Renter: может создавать бронирования; редактировать/отменять ТОЛЬКО свои (и только пока pending).
    - Landlord (владелец listing): может видеть бронирования своего listing и менять статус (approve/reject).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_renter = hasattr(user, "profile") and user.profile.role == "renter"
        is_landlord = hasattr(user, "profile") and user.profile.role == "landlord"
        is_listing_owner = obj.listing.owner_id == user.id
        is_own_booking = obj.renter_id == user.id

        if request.method in SAFE_METHODS:
            # читать может сам бронирующий или владелец объявления
            return is_own_booking or is_listing_owner

        # действия:
        action = getattr(view, 'action', None)

        # отмена бронирования самим арендатором
        if action == 'cancel' and is_own_booking:
            return True

        # approve/reject — только владелец объявления (landlord)
        if action in ('approve', 'reject') and is_landlord and is_listing_owner:
            return True

        # обновление/удаление стандартными методами: разрешим только владельцу брони и только пока pending
        if is_own_booking and obj.status == 'pending':
            return True

        return False
