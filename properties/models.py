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
    RULE_TYPES = [
        ('no_checkin', 'No Check-in'),
        ('no_checkout', 'No Check-out'),
        ('min_stay', 'Minimum Stay'),
        ('min_stay_period', 'Minimum Stay for Period'),
    ]

    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='booking_rules')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    days_of_week = models.CharField(max_length=7, blank=True, help_text="Comma-separated list of day numbers (0=Monday, 6=Sunday)")
    min_nights = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        if self.rule_type in ['no_checkin', 'no_checkout'] and not self.days_of_week:
            raise ValidationError("Days of week must be specified for no check-in/check-out rules.")
        if self.rule_type in ['min_stay', 'min_stay_period'] and self.min_nights is None:
            raise ValidationError("Minimum nights must be specified for minimum stay rules.")
        if self.rule_type == 'min_stay_period' and (not self.start_date or not self.end_date):
            raise ValidationError("Start and end dates must be specified for minimum stay period rules.")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.get_rule_type_display()} rule for {self.property}"

    class Meta:
        ordering = ['property', 'rule_type', 'start_date']

class Property(models.Model):
    WEEKEND_DAYS = [4, 5]  # Friday and Saturday

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
        
        booking_rules = self.booking_rules.all()

        # Check no check-in and no check-out rules
        for rule in booking_rules:
            if rule.rule_type == 'no_checkin' and str(check_in_date.weekday()) in rule.days_of_week.split(','):
                raise ValidationError(f"Check-in is not allowed on {check_in_date.strftime('%A')}s for this property.")
            
            if rule.rule_type == 'no_checkout' and str(check_out_date.weekday()) in rule.days_of_week.split(','):
                raise ValidationError(f"Check-out is not allowed on {check_out_date.strftime('%A')}s for this property.")

        # Get the applicable minimum stay rule
        min_stay_rule = None
        for rule in booking_rules:
            if rule.rule_type == 'min_stay':
                min_stay_rule = rule
            elif rule.rule_type == 'min_stay_period' and rule.start_date <= check_in_date <= rule.end_date:
                min_stay_rule = rule
                break  # Period-specific rule takes precedence

        # Check minimum stay and gap stays
        if min_stay_rule and nights < min_stay_rule.min_nights:
            if self.allow_gap_stays:
                prev_booking = self.bookings.filter(check_out_date__lte=check_in_date).order_by('-check_out_date').first()
                next_booking = self.bookings.filter(check_in_date__gte=check_out_date).order_by('check_in_date').first()
                
                if prev_booking and next_booking:
                    gap_size = (next_booking.check_in_date - prev_booking.check_out_date).days
                    if nights == gap_size:
                        # This is a valid gap stay
                        return
            
            # If we get here, it's not a valid booking
            raise ValidationError(f"Booking does not meet minimum stay requirement of {min_stay_rule.min_nights} nights and is not a valid gap stay.")

    class Meta:
        verbose_name_plural = "Properties"