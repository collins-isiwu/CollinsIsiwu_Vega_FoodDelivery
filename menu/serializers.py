from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    """
    Serializer for food items, used by both admin and regular users.
    """
    class Meta:
        model = Food
        fields = ['name', 'description', 'price', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FoodDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed information about a specific food item.
    """
    class Meta:
        model = Food
        fields = ['name', 'description', 'price', 'is_available', 'created_at', 'updated_at']
