from django.db import models
from utils.coordinates import get_lat_lng_from_address


class Restaurant(models.Model):
    """
    Model representing a restaurant in the system.
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255) 
    is_available = models.BooleanField(default=True)
    latitude = models.FloatField(blank=True, null=True) 
    longitude = models.FloatField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method to automatically set latitude and longitude
        based on the address using the OpenCage utility function.
        """
        if not self.latitude or not self.longitude:
            self.latitude, self.longitude = get_lat_lng_from_address(self.address)
        super(Restaurant, self).save(*args, **kwargs)
