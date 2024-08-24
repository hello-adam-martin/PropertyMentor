from rest_framework import serializers
from properties.models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'address', 'bedrooms', 'bathrooms', 'max_occupancy', 'nightly_rate', 'description']