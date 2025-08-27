import django_filters
from .models import Booking

class BookingFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    listing = django_filters.NumberFilter(field_name='listing_id', lookup_expr='exact')
    start_after = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_before = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Booking
        fields = ['status', 'listing', 'start_after', 'end_before']
