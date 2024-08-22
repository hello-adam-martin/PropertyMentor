from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'property', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('property__name', 'guest__first_name', 'guest__last_name', 'special_requests')
    date_hierarchy = 'check_in_date'
    readonly_fields = ('total_price',)

    def save_model(self, request, obj, form, change):
        obj.clean()  # Validate the booking before saving it
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Bookings'
        return super().changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Add A New Booking'
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Edit Booking'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)