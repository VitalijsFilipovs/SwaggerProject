from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    avg_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'description', 'city', 'district', 'address',
            'price', 'rooms', 'property_type', 'status', 'created_at', 'updated_at',
            'avg_rating', 'reviews_count'  # 👈
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'avg_rating', 'reviews_count']

