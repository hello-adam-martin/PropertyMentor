from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('property__name', 'guest__first_name', 'guest__last_name', 'special_requests')
    date_hierarchy = 'check_in_date'