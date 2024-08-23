from django.db import models
from owners.models import Owner
from django.core.exceptions import ValidationError

class PricingRule(models.Model):
    RULE_TYPES = [
        ('weekend', 'Weekend Pricing'),
        ('seasonal', 'Seasonal Pricing'),
        ('holiday', 'Holiday Pricing'),
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
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")
        if self.price_modifier <= 0:
            raise ValidationError("Price modifier must be greater than 0.")

    def __str__(self):
        return f"{self.get_rule_type_display()} for {self.property} ({self.price_modifier}%)"

    def get_modifier_factor(self):
        return self.price_modifier / 100

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

    def __str__(self):
        return self.name
    
    def get_price_for_date(self, date):
        base_price = self.nightly_rate
        for rule in self.pricing_rules.all():
            if rule.rule_type == 'weekend' and date.weekday() in self.WEEKEND_DAYS:
                return base_price * rule.get_modifier_factor()
            elif rule.rule_type == 'seasonal' and rule.start_date <= date <= rule.end_date:
                return base_price * rule.get_modifier_factor()
            elif rule.rule_type == 'holiday' and rule.start_date == date:  # Assuming holiday is a single day
                return base_price * rule.get_modifier_factor()
        return base_price

    class Meta:
        verbose_name_plural = "Properties"