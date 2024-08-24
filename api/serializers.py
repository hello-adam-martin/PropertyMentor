from rest_framework import serializers
from properties.models import Property
from bookings.models import Booking
from .models import WebhookSubscription

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'address', 'bedrooms', 'bathrooms', 'max_occupancy', 'nightly_rate', 'description']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'property', 'guest', 'check_in_date', 'check_out_date', 'num_guests', 'total_price', 'status']
        read_only_fields = ['total_price', 'status']

class WebhookSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookSubscription
        fields = ['id', 'event', 'target_url', 'is_active']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)