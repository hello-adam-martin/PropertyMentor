from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

class Booking(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey('guests.Guest', on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    special_requests = models.TextField(blank=True)

    def calculate_price_breakdown(self):
        breakdown = []
        if self.check_in_date and self.check_out_date and self.property:
            current_date = self.check_in_date
            while current_date < self.check_out_date:
                price, rule_applied = self.get_price_and_rule_for_date(current_date)
                breakdown.append({
                    'date': current_date,
                    'price': price,
                    'rule_applied': rule_applied
                })
                current_date += timedelta(days=1)
        return breakdown

    def get_price_and_rule_for_date(self, date):
        if not self.property:
            return Decimal('0.00'), "No property selected"

        base_price = self.property.nightly_rate
        applicable_rules = []

        for rule in self.property.pricing_rules.all():
            if rule.rule_type == 'override' and rule.start_date == date:
                return self.round_price(base_price * rule.get_modifier_factor()), f"Override: {rule.price_modifier}%"
            elif rule.rule_type == 'seasonal' and rule.start_date <= date <= rule.end_date:
                applicable_rules.append(rule)
            elif rule.rule_type == 'weekend' and date.weekday() in [4, 5]:  # Friday and Saturday
                applicable_rules.append(rule)

        if applicable_rules:
            applicable_rules.sort(key=lambda x: (x.rule_type != 'seasonal', -x.price_modifier))
            applied_rule = applicable_rules[0]
            return self.round_price(base_price * applied_rule.get_modifier_factor()), f"{applied_rule.get_rule_type_display()}: {applied_rule.price_modifier}%"

        return self.round_price(base_price), "Base rate"

    def calculate_total_price(self):
        total = sum(Decimal(day['price']) for day in self.calculate_price_breakdown())
        return self.round_price(total)

    @staticmethod
    def round_price(price):
        return Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def clean(self):
        if not self.check_in_date:
            raise ValidationError("Check-in date is required.")
        if not self.check_out_date:
            raise ValidationError("Check-out date is required.")
        if not self.property:
            raise ValidationError("Property is required.")

        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        nights = (self.check_out_date - self.check_in_date).days

        overlapping_bookings = Booking.objects.filter(
            property=self.property,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("This booking overlaps with an existing booking.")

        # Check booking rules
        try:
            self.property.check_booking_rules(self.check_in_date, self.check_out_date)
        except ValidationError as e:
            raise ValidationError(str(e))

        self.total_price = self.calculate_total_price()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest} at {self.property} ({self.check_in_date} to {self.check_out_date})"

    class Meta:
        ordering = ['-check_in_date']