from django.db import models
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant
from menu.models import Food

CustomUser = get_user_model()

class Order(models.Model):
    """
    Model representing a food order placed by a user.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    food_items = models.ManyToManyField(Food)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    courier_engaged = models.BooleanField(default=False)
    restaurant_engaged = models.BooleanField(default=False)
    distance = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    estimated_delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
