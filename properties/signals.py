from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Property
from api.webhooks import send_webhook
from api.serializers import PropertySerializer

@receiver(post_save, sender=Property)
def property_saved(sender, instance, created, **kwargs):
    if created:
        send_webhook('property_created', PropertySerializer(instance).data)
    else:
        send_webhook('property_updated', PropertySerializer(instance).data)