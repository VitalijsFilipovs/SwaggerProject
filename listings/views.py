from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter
from GlobalPagination.permissions import IsLandlordOrReadOnly
from django.db.models import Avg, Count

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated, IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description', 'city', 'district', 'address']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        base_qs = super().get_queryset() if hasattr(super(), "get_queryset") else Listing.objects.all()
        qs = base_qs.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews")
        )
        user = self.request.user
        if user.is_authenticated and hasattr(user, "profile") and user.profile.role == "landlord":
            return qs.filter(owner=user)
        return qs.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
