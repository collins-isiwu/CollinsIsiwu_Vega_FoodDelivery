from rest_framework import serializers
from .models import Food, FoodRating, FoodComment
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

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
    average_rating = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'description', 'price', 'is_available', 'average_rating', 'comments']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_comments(self, obj):
        comments = obj.comments.all()
        return [{'user': comment.user.first_name, 'comment': comment.comment} for comment in comments]
    

class FoodRatingSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = FoodRating
        fields = ['food', 'rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        food = validated_data['food']
        rating_value = validated_data['rating']

        # Check if the user has already rated this food
        existing_rating = FoodRating.objects.filter(user=user, food=food).first()

        if existing_rating:
            # Update the existing rating
            existing_rating.rating = rating_value
            existing_rating.save()
            return existing_rating
        else:
            return FoodRating.objects.create(user=user, food=food, rating=rating_value)


class FoodCommentSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = FoodComment
        fields = ['food', 'comment']

