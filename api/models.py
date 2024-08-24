from django.db import models
from django.contrib.auth.models import User

class WebhookSubscription(models.Model):
    EVENT_CHOICES = [
        ('booking_created', 'Booking Created'),
        ('booking_updated', 'Booking Updated'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('property_created', 'Property Created'),
        ('property_updated', 'Property Updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webhook_subscriptions')
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    target_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'event', 'target_url')

    def __str__(self):
        return f"{self.user.username} - {self.get_event_display()} - {self.target_url}"

    @classmethod
    def get_available_events(cls):
        return dict(cls.EVENT_CHOICES)