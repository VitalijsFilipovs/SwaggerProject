from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'rooms', 'property_type', 'status', 'owner', 'created_at')
    list_filter = ('city', 'property_type', 'status', 'rooms')
    search_fields = ('title', 'description', 'city', 'district', 'address', 'owner__username', 'owner__email')
