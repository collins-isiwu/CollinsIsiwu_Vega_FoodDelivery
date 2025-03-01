from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, updating, and viewing restaurant details.
    """
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'created_at', 'updated_at']
