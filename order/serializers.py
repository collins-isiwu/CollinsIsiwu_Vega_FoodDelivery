from rest_framework import serializers
from .models import Order
from menu.models import Food
from .utils import find_nearest_restaurant
from .tasks import engage_restaurant_and_courier
from django.utils import timezone
from datetime import timedelta

class OrderCreateSerializer(serializers.ModelSerializer):
    food_item_ids = serializers.ListField(write_only=True)  
    address = serializers.CharField(write_only=True) 

    restaurant = serializers.SerializerMethodField() 
    total_price = serializers.ReadOnlyField()
    estimated_delivery_time = serializers.ReadOnlyField()
    distance = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['food_item_ids', 'restaurant', 'food_item_ids', 'distance', 'total_price', 'status', 'address', 'estimated_delivery_time']

    def get_restaurant(self, obj):
        """
        Return a serializable representation of the restaurant.
        """
        return {
            'name': obj.restaurant.name,
            'address': obj.restaurant.address,
            'is_available': obj.restaurant.is_available,
        }

    def create(self, validated_data):
        user = self.context['request'].user
        address = validated_data.pop('address')

        nearest_restaurant, distance = find_nearest_restaurant(address)

        if not nearest_restaurant:
            raise serializers.ValidationError({"restaurant": "No restaurant available near the specified location."})

        food_item_ids = validated_data.pop('food_item_ids')
        food_items = Food.objects.filter(id__in=food_item_ids)

        if not food_items.exists():
            raise serializers.ValidationError({"food_items": "Invalid or empty food item list provided."})

        total_price = sum(item.price for item in food_items)

        # Create the order
        order = Order.objects.create(
            user=user,
            restaurant=nearest_restaurant,
            total_price=total_price,
            status='Pending',
            distance=distance,
            estimated_delivery_time=timezone.now() + timedelta(minutes=15)
        )
        order.food_items.set(food_items)

        # Engage restaurant and courier using Celery task
        engage_restaurant_and_courier.delay(order.id)

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    food_items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = ['restaurant_name', 'food_items', 'distance','total_price', 'status','estimated_delivery_time']


class OrderListSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'food_items','restaurant_name', 'distance', 'total_price', 'status', 'created_at', 'updated_at', 'estimated_delivery_time']
