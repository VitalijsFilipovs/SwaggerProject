import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='exact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    property_type = django_filters.CharFilter(field_name='property_type', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Listing
        fields = ['city', 'rooms', 'property_type', 'status', 'price_min', 'price_max']
