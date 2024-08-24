from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from api.webhooks import send_webhook
from api.serializers import BookingSerializer

@receiver(post_save, sender=Booking)
def booking_saved(sender, instance, created, **kwargs):
    if created:
        send_webhook('booking_created', BookingSerializer(instance).data)
    else:
        if instance.status == 'cancelled':
            send_webhook('booking_cancelled', BookingSerializer(instance).data)
        else:
            send_webhook('booking_updated', BookingSerializer(instance).data)