from django.contrib import admin
from .models import Booking
from django.utils.html import format_html

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('property__name', 'guest__first_name', 'guest__last_name', 'special_requests')
    readonly_fields = ('total_price', 'price_breakdown')

    def price_breakdown(self, obj):
        if not obj.pk:  # If the object hasn't been saved yet
            return "Price breakdown will be available after saving."

        breakdown = obj.calculate_price_breakdown()
        if not breakdown:
            return "Unable to calculate price breakdown. Please ensure all required fields are filled."

        html = "<table><tr><th>Date</th><th>Price</th><th>Rule Applied</th></tr>"
        for day in breakdown:
            html += f"<tr><td>{day['date']}</td><td>${day['price']}</td><td>{day['rule_applied']}</td></tr>"
        html += f"<tr><td colspan='3'><strong>Total: ${obj.total_price}</strong></td></tr>"
        html += "</table>"
        return format_html(html)
    price_breakdown.short_description = "Price Breakdown"

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new booking
            obj.total_price = 0  # Initialize total_price to 0
        obj.full_clean()  # This will run the validation and calculate the price
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If this is an existing object
            return self.readonly_fields
        return ('total_price',)  # Only make total_price readonly for existing objects