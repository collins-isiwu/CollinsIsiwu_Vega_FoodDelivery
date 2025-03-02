from django.db import models
from users.models import CustomUser
class Food(models.Model):
    """
    Model representing a food item on the menu.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        """Return the average rating of the food item."""
        ratings = self.ratings.all() 
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return None 


class FoodRating(models.Model):
    """
    Model for food rating.
    """
    food = models.ForeignKey(Food, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='food_ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating from 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('food', 'user')

    def __str__(self):
        return f'{self.food.name} - {self.rating} stars'


class FoodComment(models.Model):
    """
    Model for food comments.
    """
    food = models.ForeignKey(Food, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='food_comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.email} on {self.food.name}'
    
    