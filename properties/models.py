from django.db import models
from django.core.exceptions import ValidationError
from owners.models import Owner
from decimal import Decimal

class PricingRule(models.Model):
    RULE_TYPES = [
        ('weekend', 'Weekend Pricing'),
        ('seasonal', 'Seasonal Pricing'),
        ('override', 'Override Pricing'),
    ]

    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='pricing_rules')
    rule_type = models.CharField(max_length=10, choices=RULE_TYPES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price_modifier = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Enter a percentage. E.g., 120 for 20% increase, 80 for 20% discount"
    )

    def clean(self):
        if self.rule_type == 'seasonal' and (not self.start_date or not self.end_date):
            raise ValidationError("Seasonal pricing must have start and end dates.")
        if self.rule_type == 'override' and not self.start_date:
            raise ValidationError("Override pricing must have a start date.")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")
        if self.price_modifier <= 0:
            raise ValidationError("Price modifier must be greater than 0.")

    def __str__(self):
        return f"{self.get_rule_type_display()} for {self.property} ({self.price_modifier}%)"

    def get_modifier_factor(self):
        return self.price_modifier / Decimal('100')

class BookingRule(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='booking_rules')
    start_date = models.DateField()
    end_date = models.DateField()
    min_nights = models.PositiveIntegerField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")
        if self.min_nights <= 0:
            raise ValidationError("Minimum nights must be a positive number.")

    def __str__(self):
        return f"Minimum stay of {self.min_nights} nights for {self.property} from {self.start_date} to {self.end_date}"

    class Meta:
        ordering = ['property', 'start_date']

class Property(models.Model):
    WEEKEND_DAYS = [4, 5]  # Friday and Saturday
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    max_occupancy = models.PositiveIntegerField()
    nightly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    allow_gap_stays = models.BooleanField(default=True, help_text="Allow bookings shorter than the minimum stay to fill gaps between bookings")
    no_checkin_days = models.CharField(max_length=7, blank=True, help_text="Days when check-in is not allowed")
    no_checkout_days = models.CharField(max_length=7, blank=True, help_text="Days when check-out is not allowed")
    minimum_stay = models.PositiveIntegerField(default=1, help_text="Minimum number of nights required for a booking")

    def __str__(self):
        return self.name
    
    def get_price_for_date(self, date):
        base_price = self.nightly_rate
        applicable_rules = []

        for rule in self.pricing_rules.all():
            if rule.rule_type == 'override' and rule.start_date == date:
                return base_price * rule.get_modifier_factor()  # Highest priority, return immediately
            elif rule.rule_type == 'seasonal' and rule.start_date <= date <= rule.end_date:
                applicable_rules.append(rule)
            elif rule.rule_type == 'weekend' and date.weekday() in self.WEEKEND_DAYS:
                applicable_rules.append(rule)

        if applicable_rules:
            # Sort by rule type (seasonal before weekend) and then by modifier (highest modifier first)
            applicable_rules.sort(key=lambda x: (x.rule_type != 'seasonal', -x.price_modifier))
            return base_price * applicable_rules[0].get_modifier_factor()

        return base_price
    
    def check_booking_rules(self, check_in_date, check_out_date):
        nights = (check_out_date - check_in_date).days
        
        # Check no check-in and no check-out rules
        if str(check_in_date.weekday()) in self.no_checkin_days:
            raise ValidationError(f"Check-in is not allowed on {check_in_date.strftime('%A')}s for this property.")
        
        if str(check_out_date.weekday()) in self.no_checkout_days:
            raise ValidationError(f"Check-out is not allowed on {check_out_date.strftime('%A')}s for this property.")

        # Check minimum stay rules
        min_stay = self.minimum_stay
        for rule in self.booking_rules.all():
            if rule.start_date <= check_in_date <= rule.end_date:
                min_stay = max(min_stay, rule.min_nights)
                break

        if nights < min_stay:
            if self.allow_gap_stays:
                prev_booking = self.bookings.filter(check_out_date__lte=check_in_date).order_by('-check_out_date').first()
                next_booking = self.bookings.filter(check_in_date__gte=check_out_date).order_by('check_in_date').first()
                
                if prev_booking and next_booking:
                    gap_size = (next_booking.check_in_date - prev_booking.check_out_date).days
                    if nights == gap_size:
                        # This is a valid gap stay
                        return
            
            # If we get here, it's not a valid booking
            raise ValidationError(f"Booking does not meet minimum stay requirement of {min_stay} nights and is not a valid gap stay.")

    class Meta:
        verbose_name_plural = "Properties"