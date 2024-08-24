from django.contrib import admin
from .models import Booking
from django.utils.html import format_html
from decimal import Decimal

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'check_in_date', 'check_out_date', 'num_guests', 'base_total', 'fees_total', 'total_price', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('property__name', 'guest__first_name', 'guest__last_name', 'special_requests')
    readonly_fields = ('base_total', 'fees_total', 'total_price', 'price_breakdown')

    def price_breakdown(self, obj):
        if not obj.pk:  # If the object hasn't been saved yet
            return "Price breakdown will be available after saving."

        breakdown = obj.calculate_price_breakdown()
        if not breakdown:
            return "Unable to calculate price breakdown. Please ensure all required fields are filled."

        nights = len(breakdown)
        incorporated_fees_total = Decimal('0.00')
        incorporated_fees = []

        # Calculate total incorporated fees and adjust nightly rates
        for fee in obj.property.fees.all():
            if fee.display_strategy == 'incorporated':
                fee_amount = obj.calculate_fee_amount(fee)
                incorporated_fees_total += fee_amount
                incorporated_fees.append((fee.name, fee_amount))

        fee_per_night = incorporated_fees_total / nights if nights > 0 else Decimal('0.00')

        html = "<table><tr><th>Date</th><th>Base Price</th><th>Adjusted Price</th><th>Rule Applied</th></tr>"
        for day in breakdown:
            base_price = Decimal(day['price'])
            adjusted_price = base_price + fee_per_night
            html += f"<tr><td>{day['date']}</td><td>${base_price:.2f}</td><td>${adjusted_price:.2f}</td><td>{day['rule_applied']}</td></tr>"

        html += f"<tr><td colspan='4'><strong>Base Total: ${obj.base_total:.2f}</strong></td></tr>"
        
        # Add fee breakdown
        html += "<tr><td colspan='4'><strong>Fees:</strong></td></tr>"
        for fee in obj.property.fees.all():
            fee_amount = obj.calculate_fee_amount(fee)
            if fee.display_strategy == 'incorporated':
                html += f"<tr><td colspan='3'>{fee.name}</td><td>${fee_amount:.2f} (incorporated)</td></tr>"
            else:
                html += f"<tr><td colspan='3'>{fee.name}</td><td>${fee_amount:.2f}</td></tr>"
        
        html += f"<tr><td colspan='4'><strong>Fees Total: ${obj.fees_total:.2f}</strong></td></tr>"
        html += f"<tr><td colspan='4'><strong>Grand Total: ${obj.total_price:.2f}</strong></td></tr>"
        html += "</table>"

        if incorporated_fees:
            html += "<p><strong>Note:</strong> The following fees have been incorporated into the nightly rates:</p>"
            html += "<ul>"
            for fee_name, fee_amount in incorporated_fees:
                html += f"<li>{fee_name}: ${fee_amount:.2f} (${fee_amount/nights:.2f} per night)</li>"
            html += "</ul>"

        return format_html(html)

    price_breakdown.short_description = "Price Breakdown"

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # This will run the validation and calculate the price
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If this is an existing object
            return self.readonly_fields
        return ('base_total', 'fees_total', 'total_price', 'price_breakdown')  # Make these fields readonly for new objects too

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:  # This is an add form
            fieldsets = [
                (None, {
                    'fields': ['property', 'guest', 'check_in_date', 'check_out_date', 'num_guests', 'status', 'special_requests']
                }),
            ]
        else:  # This is a change form
            fieldsets = [
                (None, {
                    'fields': ['property', 'guest', 'check_in_date', 'check_out_date', 'num_guests', 'status', 'special_requests']
                }),
                ('Price Information', {
                    'fields': ['base_total', 'fees_total', 'total_price', 'price_breakdown'],
                }),
            ]
        return fieldsets