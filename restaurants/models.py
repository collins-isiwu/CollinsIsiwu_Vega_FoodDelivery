from django.db import models

class Restaurant(models.Model):
    """
    Model representing a restaurant in the system.
    """
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
