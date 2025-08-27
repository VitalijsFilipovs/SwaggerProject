import django_filters
from .models import Review

class ReviewFilter(django_filters.FilterSet):
    listing = django_filters.NumberFilter(field_name="listing_id", lookup_expr="exact")
    user = django_filters.NumberFilter(field_name="user_id", lookup_expr="exact")
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="lte")

    class Meta:
        model = Review
        fields = ["listing", "user", "min_rating", "max_rating"]
