from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'bedrooms', 'bathrooms', 'max_occupancy', 'nightly_rate')
    list_filter = ('bedrooms', 'bathrooms', 'max_occupancy')
    search_fields = ('name', 'address', 'owner__first_name', 'owner__last_name')