from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Booking
from .serializers import BookingSerializer
from .filters import BookingFilter
from .permissions import BookingAccessPermission
from listings.models import Listing

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, BookingAccessPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookingFilter
    ordering_fields = ['start_date', 'end_date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        # Landlord видит брони на СВОИ listing'и; Renter — свои заявки
        if hasattr(user, "profile") and user.profile.role == "landlord":
            my_listing_ids = Listing.objects.filter(owner=user).values_list('id', flat=True)
            return Booking.objects.filter(listing_id__in=my_listing_ids)
        return Booking.objects.filter(renter=user)

    def perform_create(self, serializer):
        # Создаёт только renter
        user = self.request.user
        if not (hasattr(user, "profile") and user.profile.role == "renter"):
            raise PermissionError("Только арендатор может создавать бронирование.")
        serializer.save(renter=user, status='pending')

    # ----- кастомные действия -----

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.status not in ('pending',):
            return Response({"detail": "Можно подтвердить только бронирование со статусом pending."},
                            status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'approved'
        booking.save(update_fields=['status'])
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if booking.status not in ('pending',):
            return Response({"detail": "Можно отклонить только бронирование со статусом pending."},
                            status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'rejected'
        booking.save(update_fields=['status'])
        return Response({"status": "rejected"})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        # отменять может только сам renter; проверка — в permission
        if booking.status in ('cancelled', 'rejected'):
            return Response({"detail": "Бронирование уже отменено/отклонено."},
                            status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save(update_fields=['status'])
        return Response({"status": "cancelled"})
