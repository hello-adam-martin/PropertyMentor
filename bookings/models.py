from django.db import models
from django.core.exceptions import ValidationError
from properties.models import Property
from guests.models import Guest
from datetime import timedelta

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
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

    def __str__(self):
        return f"{self.guest} at {self.property} ({self.check_in_date} to {self.check_out_date})"

    def calculate_total_price(self):
        if self.check_in_date and self.check_out_date:
            total_price = 0
            current_date = self.check_in_date
            while current_date < self.check_out_date:
                total_price += self.property.get_price_for_date(current_date)
                current_date += timedelta(days=1)
            return total_price
        return 0

    def clean(self):
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

            if self.check_out_date == self.check_in_date:
                raise ValidationError("Check-out date cannot be the same as check-in date.")

            overlapping_bookings = Booking.objects.filter(
                property=self.property,
                check_in_date__lt=self.check_out_date,
                check_out_date__gt=self.check_in_date
            ).exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError("This booking overlaps with an existing booking.")

        self.total_price = self.calculate_total_price()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['check_in_date']
        verbose_name_plural = "Bookings"