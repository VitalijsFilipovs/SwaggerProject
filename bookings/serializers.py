from rest_framework import serializers
from .models import Booking
from listings.models import Listing
from django.db.models import Q

class BookingSerializer(serializers.ModelSerializer):
    renter = serializers.ReadOnlyField(source='renter.username')

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'renter', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['id', 'renter', 'status', 'created_at']

    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        listing = attrs.get('listing')

        if start >= end:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания.")

        # Нельзя бронировать деактивированное объявление
        if listing.status != 'active':
            raise serializers.ValidationError("Нельзя бронировать неактивное объявление.")

        # Проверка пересечений только с утверждёнными бронированиями
        overlaps = Booking.objects.filter(
            listing=listing,
            status='approved'
        ).filter(
            Q(start_date__lt=end) & Q(end_date__gt=start)  # пересечение диапазонов
        )
        if overlaps.exists():
            raise serializers.ValidationError("На эти даты уже есть подтверждённое бронирование.")
        return attrs
