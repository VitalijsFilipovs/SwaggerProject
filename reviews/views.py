from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Review
from .serializers import ReviewSerializer
from .filters import ReviewFilter
from .permissions import IsReviewOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("listing", "user")
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["created_at", "rating"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
